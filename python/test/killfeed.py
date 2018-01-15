import overwatch as OW
import cv2
import numpy as np
from utils import image as ImageUtils
import skimage
import heapq
from operator import itemgetter
from skimage import measure

class Killfeed:
    def __init__(self, frame, index):
        # player and chara might be different from analysis of current frame!
        # Thus extra variables needed.

        # Killer/Resurrector (On left side)
        self.player1 = {
            "chara": "empty",   # name of chara, or "empty"
            "player": "empty",  #name of player, or "empty"
            "team": "empty",   # name of team, or "empty"
            "pos": -1
        }

        # Killed/Resurrected (On right side)
        self.player2 = {
            "chara": "empty",
            "player": "empty",
            "team": "empty",
            "pos": -1
        }

        # ability code, see overwatch.py line 282
        self.ability = 0

        # List of assisting players, with the form of a dict:
        # {
        #     "chara": "empty",
        #     "player": "empty",
        #     "team": "empty"
        # }
        self.assists = []

        # Row number of current killfeed, ranges from 0 to 5.
        self.index = index
        # Tell if the killfeed is valid, mostly for convenience.
        self.is_valid = False

        self.frame = frame
        self.game_type = frame.game.game_type

        # Get row image
        killfeed_pos = OW.get_killfeed_pos(index)[frame.game.game_type]
        killfeed_with_gap_pos = OW.get_killfeed_with_gap_pos(index)[frame.game.game_type]
        self.image = ImageUtils.crop(frame.image, killfeed_pos)
        self.image_with_gap = ImageUtils.crop(frame.image, killfeed_with_gap_pos)
        self.get_players()
        self.get_assists()

    def get_players(self):
        """
        Get killfeed in a row.
        @Author: Appcell, adapted from code by Leavebody, furtherly adapted from
                 code by Appcell
        @return: None
        """
        edge_validation = self._validate_edge()
        icons_weights = self._get_icons_weights(edge_validation)
        # TODO Only need two best matches in the end. Kept three while debugging.
        icons_weights = sorted(icons_weights, key = itemgetter('prob'), reverse = True)
        best_matches = icons_weights[0:3]

        # There should be a vertical edge
        # between left 3 pixels to the icon
        # and right 1 pixel to the icon
        # with no more than 2 pixels in the vertical line missing.
        # A vertical line should have a width of no more than 2.
        matched = list(filter(
            lambda x: x['prob'] >= OW.KILLFEED_MAX_PROB[self.game_type] and edge_validation[x['pos']] == True,
            best_matches))

        if len(matched) == 0:
            self.is_valid = False
        elif len(matched) == 1:
            # If only one icon gets recognized, it has to be on right side.
            if matched[0].x < OW.KILLFEED_WIDTH[self.game_type] - OW.KILLFEED_RIGHT_WIDTH[self.game_type]:
                self.is_valid = False
            else:
                self.is_valid = True
                self.player2 = self._set_player_info(matched[0], 'right')
        else:
            self.is_valid = True
            if matched[0]['pos'] < matched[1]['pos']:
                self.player1 = self._set_player_info(matched[0], 'left')
                self.player2 = self._set_player_info(matched[1], 'right')
            else:
                self.player2 = self._set_player_info(matched[0], 'right')
                self.player1 = self._set_player_info(matched[1], 'left')


    def _validate_edge(self):
        """
        Find vertical edges in killfeed image,
        and use the edges to get the possible icon positions.
        @return: A list of boolean, result[i] is True if there can be a icon starting from x=i,
                and result[i] is false if x=i can starts an icon.
        """
        # Generate edged image for this killfeed row.
        edge_image = cv2.Canny(self.image, 100, 200)  
        # Get the "spanned" edge image.
        edge_span = (edge_image.sum(0) + np.roll(edge_image.sum(0), 1))/255
        # Sum on y axis and normalize
        edge_sum = edge_span.astype('float') / OW.KILLFEED_ICON_HEIGHT[self.game_type]
        edge_validation = [False, False]
        # truecount = 0
        for i in range(2, OW.KILLFEED_WIDTH[self.game_type] - 38):
            edge_scores_left = edge_sum[i-2: i+2]
            edge_scores_right = edge_sum[i+33: i+37]

            if (max(edge_scores_left) >= OW.KILLFEED_ICON_EDGE_HEIGHT_RATIO_LEFT[self.game_type] and
            max(edge_scores_right) >= OW.KILLFEED_ICON_EDGE_HEIGHT_RATIO_RIGHT[self.game_type]):
                # The metric is that there should be a vertical edge
                # between left 3 pixels to the icon position
                # and right 1 pixel to the icon position
                # with no more than 2 pixels in the vertical line missing.
                # A vertical line should have a width of no more than 2.
                edge_validation.append(True)
            else:
                edge_validation.append(False)
        edge_validation.extend([False]*6)

        return edge_validation

    def _set_player_info(self, player, position):
        res = {'chara': player['chara'], 'pos': player['pos']}
        color_pos = OW.get_killfeed_team_color_pos(player['pos'], position)[self.game_type]
        cv2.imshow('t',self.image)
        cv2.waitKey(0)

        color = self.image[color_pos[0], color_pos[1]]
        colors_ref = {}
        if self.frame.game.team_colors is not None:
            colors_ref = self.frame.game.team_colors
        else:
            colors_ref = self.frame.get_team_colors()
        dist_left = ImageUtils.color_distance_normalized(color, colors_ref['left'])
        dist_right = ImageUtils.color_distance_normalized(color, colors_ref['right'])
        print [color_pos[0], color_pos[1]]
        print colors_ref
        print color
        print [dist_left, dist_right]
        print "==========="
        res['team'] = self.frame.game.team_names['left'] \
                             if dist_left < dist_right else self.frame.game.team_names['right']

        chara = OW.get_chara_name(player['chara'])

        if res['team'] == self.frame.game.team_names['left']:
            res['player'] = next((item.name for item in self.frame.players[0:6] if item.chara == chara), "empty")
        else:
            res['player'] = next((item.name for item in self.frame.players[6:12] if item.chara == chara), "empty")

        return res
    
    def _set_assist_info(self, assist):
        res = {
        'chara': assist['chara'],
        'player': 'empty',
        'team': assist['team']
        }

        if assist['team'] == self.frame.game.team_names['left']:
            for player in self.frame.players[0:6]:
                if player.chara == assist['chara']:
                    res['player'] = player.name
        else:
            for player in self.frame.players[6:12]:
                if player.chara == assist['chara']:
                    res['player'] = player.name
        return res

    def _get_icons_weights(self, edge_validation):
        """
        Get possible icon and their weights in the killfeed image.
        @param killfeed_image: The killfeed image.
        @param edge_validation: A list of boolean. Should be the result of _validate_edge()
        @param name:
        @return: A list of KillfeedIconMatch object, which includes all possible icons in this killfeed image.
        """
        valid_pixel_count = edge_validation.count(True)
        if valid_pixel_count <= 7:
            return self._get_icons_weights_discrete(edge_validation)
        else:
            return self._get_icons_weights_full(edge_validation)

    def _get_icons_weights_full(self, edge_validation):
        """
        Use match template in cv2 to get possible icon and their weights in the killfeed image.
        @param killfeed_image: The killfeed image.
        @param edge_validation: A list of booleans. Should be the result of _validate_edge()
        @return: A list of KillfeedIconMatch object, which includes all possible icons in this killfeed image.
        """
        result = []
        for (chara, icon) in self.frame.game.killfeed_icons_ref.iteritems():
            match_result = cv2.matchTemplate(self.image, icon, cv2.TM_CCOEFF_NORMED)

            # Find two most possible location of this character's icon in the killfeed image.
            # Mask the pixels around the first location to find the second one.
            _, max_val, _, max_loc = cv2.minMaxLoc(match_result)
            if edge_validation[max_loc[0]]:
                result.append({
                    'chara': chara,
                    'prob': max_val,
                    'pos': max_loc[0]
                    })

            half_mask_width = 5
            mask_index_left = max((max_loc[0] - half_mask_width, 0))
            mask_index_right = min((max_loc[0] + half_mask_width + 1,
                                    OW.KILLFEED_WIDTH[self.game_type] - OW.KILLFEED_ICON_WIDTH[self.game_type]))
            match_result_masked = np.matrix(match_result)
            match_result_masked[0:match_result_masked.shape[0], mask_index_left: mask_index_right] = -1

            _, max_val2, _, max_loc2 = cv2.minMaxLoc(match_result_masked)

            if edge_validation[max_loc2[0]]:
                result.append({
                    'chara': chara,
                    'prob': max_val2,
                    'pos': max_loc2[0]
                    })

        return result

    def _get_icons_weights_discrete(self, edge_validation):
        """
        An alternate way to get weights of icons. Only matches the icon where the pixel passes edge validation.
        Experiments show that when there are less than 8 valid pixels in edge_validation,
        it's faster than _get_icons_weights_full().
        @param killfeed_image: The killfeed image.
        @param edge_validation: A list of boolean. Should be the result of _validate_edge()
        @param chara:
        @return: A list of KillfeedIconMatch object, which includes all possible icons in this killfeed image.
        """
        result_raw = []
        for x in range(len(edge_validation)):
            if not edge_validation[x]:
                continue
            to_compare = util.crop_by_limit(killfeed_image, 0, OW.KILLFEED_ICON_HEIGHT[self.game_type], x, OW.KILLFEED_ICON_WIDTH[self.game_type])
            best_score = -1
            best_chara = ""
            for (object_chara, object_icon) in self.icons.ICONS_CHARACTER.iteritems():
                score = self._match_template_score(to_compare, object_icon)
                if score > best_score:
                    best_score = score
                    best_chara = object_chara
                    result_raw.append({
                            'chara': best_chara,
                            'prob': best_score,
                            'pos': x
                            })
        mask = [False] * len(edge_validation)
        result_raw = sorted(result_raw, key = itemgetter('prob'), reverse = True)
        result = []
        for match in result_raw:
            if mask[match.x]:
                continue
            mask_left_index = max(0, match.x - 5)
            mask_right_index = min(len(mask), match.x + 5)
            mask[mask_left_index:mask_right_index] = [True]*(mask_right_index-mask_left_index)
            result.append(match)

        return result

    def get_assists(self):
        if self.player1['pos'] == -1 or self.player2['pos'] == -1:
            return
        distance = self.player2['pos'] - self.player1['pos'] - OW.KILLFEED_ICON_WIDTH[self.game_type]
        gap = ImageUtils.crop(self.image_with_gap, 
              [0, self.image_with_gap.shape[0], self.player1['pos'], distance])

        ability_icon = ImageUtils.crop(self.image_with_gap, 
                       OW.get_ability_icon_pos(self.player1['pos'], self.player2['pos'])[self.game_type])

        
        assist_num = int((distance - OW.ABILITY_GAP_NORMAL[self.game_type]) / OW.ASSIST_GAP[self.game_type]) - 1
        
        ability_list = OW.ABILITY_LIST[self.player1['chara']]
        ability_icons_ref = self.frame.game.ability_icons_ref[self.player1['chara']]

        if (distance - OW.ABILITY_GAP_NORMAL[self.game_type]) % OW.ASSIST_GAP[self.game_type] > 5:
            # Has ability icon
            max_prob = -10
            max_ind = 0
            for (ind, ability_index) in enumerate(ability_list):
                filtered_icon = self._preprocess_ability_icon(ability_icon)
                s = measure.compare_ssim(filtered_icon, ability_icons_ref[ind], multichannel=True)
                if s > max_prob:
                    max_prob = s
                    self.ability = ability_index
                    max_ind = ind

            if max_prob < 0.1 and self.player1['chara'] == OW.GENJI:
                self.ability = OW.ABILITY_E


        for i in range(assist_num):
            # TODO: write this into ow.py!
            assist_icon = ImageUtils.crop(self.image, 
                [OW.ABILITY_ICON_Y_MIN[self.game_type], 
                 OW.ASSIST_ICON_HEIGHT[self.game_type], 
                 8 + self.player1['pos'] + i * OW.ASSIST_GAP[self.game_type] + OW.KILLFEED_ICON_WIDTH[self.game_type], 
                 OW.ASSIST_ICON_WIDTH[self.game_type]])

            assist = {
                "chara": "empty",
                "player": "empty",
                "team": self.player1['team']
            }
            max_score = -10
            for (chara, icon) in self.frame.game.assist_icons_ref.iteritems():
                s = measure.compare_ssim(assist_icon, icon, multichannel=True)
                if s > max_score:
                    max_score = s
                    assist['chara'] = chara

            self.assists.append(self._set_assist_info(assist))

    def _preprocess_ability_icon(self, icon):

        ability_pos = OW.get_ability_icon_pos(self.player1['pos'], 
                        self.player2['pos'])[self.game_type]
        color = self.image_with_gap[ability_pos[0] + ability_pos[1]/2, ability_pos[2] + ability_pos[3] + 6]
        filtered_icon = np.zeros((icon.shape[0], icon.shape[1]))
        # There must be a better way for this
        for i in range(icon.shape[0]):
            for j in range(icon.shape[1]):
                if ImageUtils.color_distance(icon[i, j, :], color) < OW.ABILITY_ICON_COLOR_FILTER_THRESHOLD[self.game_type]:
                    filtered_icon[i, j] = 255

        return filtered_icon.astype('uint8')





