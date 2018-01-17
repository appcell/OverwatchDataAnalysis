import cv2
import numpy as np
from operator import itemgetter
from skimage import measure

import overwatch as OW
from utils import image as ImageUtils


class Killfeed:
    """Class of a Killfeed object.

    Contains info in one killfeed row.
    Player and chara might be different from analysis of current frame, thus
    extra variables needed.

    Attributes:
        player1: Killer/Resurrector (On left side)
        player2: Killed/Resurrected (On right side)
        ability: ability code, see overwatch.py line 282
        assists: list of assisting players, with the form of a dict:
                 {
                     "chara": "empty",
                     "player": "empty",
                     "team": "empty"
                 }        
        index: row number of current killfeed, ranges from 0 to 5.
        is_valid: tell if the killfeed is valid, mostly for convenience only
        is_headshot: if the elimination is by a headshot
        frame: the Frame instance who fathers this killfeed
        game_type: type of this game, can be OW.CAMETYPE_OWL or
            OW.GAMETYPE_CUSTOM
        image: image of killfeed row, without gap
        image_with_gap: image of killfeed row, with gap
    """

    def __init__(self, frame, index):
        """Initialize a Killfeed object.

        Author:
            Appcell

        Args:
            frame: the Frame obj current killfeed is in
            index: row number of current killfeed, ranges from 0 to 5.

        Returns:
            None 
        """
        self.player1 = {
            "chara": "empty",   # name of chara, or "empty"
            "player": "empty",  # name of player, or "empty"
            "team": "empty",   # name of team, or "empty"
            "pos": -1
        }
        self.player2 = {
            "chara": "empty",
            "player": "empty",
            "team": "empty",
            "pos": -1
        }
        self.ability = 0
        self.assists = []
        self.index = index
        self.is_valid = True
        self.is_headshot = False
        self.frame = frame
        self.game_type = frame.game.game_type

        killfeed_pos = OW.get_killfeed_pos(index)[frame.game.game_type]
        killfeed_with_gap_pos = OW.get_killfeed_with_gap_pos(index)[
            frame.game.game_type]
        self.image = ImageUtils.crop(frame.image, killfeed_pos)
        self.image_with_gap = ImageUtils.crop(
            frame.image, killfeed_with_gap_pos)

        self.get_players()
        self.get_ability_and_assists()
        self.get_headshot()

    def __eq__(self, other):
        if self.player1['chara'] == other.player1['chara'] \
            and self.player2['chara'] == other.player2['chara'] \
            and self.player1['team'] == other.player1['team'] \
            and self.player2['team'] == other.player2['team']:
            return True
        return False

    def get_players(self):
        """Get 2 (or 1) player(s) info in a killfeed row.

        Crop row image from frame, then do template matching with all given
        avatar references on it. The ones with maximum scores are final 
        recognition results. Since there're usually 2 avatars in a row, 
        matching results have to be split into left/right groups before further
        processing.

        Author:
            Appcell, Leavebody

        Args:
            None

        Returns:
            None 
        """
        edge_validation = self._validate_edge()
        icons_weights = self._get_icons_weights(edge_validation)

        if not icons_weights:
            self.is_valid = False
            return

        # Differentiate results from 2 sides first
        mean_pos = np.mean([i['pos'] for i in icons_weights])
        icons_weights_left = [i for i in icons_weights if i['pos'] < mean_pos]
        icons_weights_right = [i for i in icons_weights if i['pos'] > mean_pos]
        mean_pos_left = np.mean([i['pos'] for i in icons_weights_left])
        mean_pos_right = np.mean([i['pos'] for i in icons_weights_right])

        if mean_pos_right < OW.KILLFEED_WIDTH[self.game_type] \
            - OW.KILLFEED_RIGHT_WIDTH[self.game_type]:
            self.is_valid = False
            return

        if abs(mean_pos_right - mean_pos_left) \
            < OW.KILLFEED_ICON_WIDTH[self.game_type] - 7:
            # Only one icon exists
            matched = self._get_matched_icon(icons_weights, edge_validation)
            if matched and matched[0]['pos'] \
                >= OW.KILLFEED_WIDTH[self.game_type] \
                - OW.KILLFEED_RIGHT_WIDTH[self.game_type]:
                self.player2 = self._set_player_info(matched[0], 'right')
        else:
            # 2 icons got recognized
            icons_weights_left = sorted(icons_weights_left,
                                        key=itemgetter('prob'), reverse=True)[0:2]
            icons_weights_right = sorted(icons_weights_right,
                                         key=itemgetter('prob'), reverse=True)[0:2]
            if icons_weights_left:
                self.player1 = self._set_player_info(icons_weights_left[0], 'left')
            if icons_weights_right:
                self.player2 = self._set_player_info(icons_weights_right[0], 'right')

        if self.player2['pos'] == -1:
            self.is_valid = False


    def _validate_edge(self):
        """Get a list of possible icon positions.

        There should be a vertical edge between left 3 pixels to the icon and
        right 1 pixel to the icon with no more than 2 pixels in the vertical 
        line missing. A vertical line should have a width of no more than 2.

        Find vertical edges in killfeed image, and use the edges to get the 
        possible icon positions.

        Author:
            Leavebody, Appcell

        Args:
            None

        Returns:
            A list of boolean, result[i] is True if there can be a icon 
            starting from x=i, and result[i] is false if x=i can starts
            an icon.
        """
        # Generate edged image for this killfeed row.
        edge_image = cv2.Canny(self.image, 100, 200)

        # Get the "spanned" edge image.
        edge_span = (edge_image.sum(0) + np.roll(edge_image.sum(0), 1))/255
        # Sum on y axis and normalize
        edge_sum = edge_span.astype(
            'float') / OW.KILLFEED_ICON_HEIGHT[self.game_type]
        edge_validation = [False, False]

        for i in range(2, OW.KILLFEED_WIDTH[self.game_type] - 38):
            edge_scores_left = edge_sum[i-2: i+2]
            edge_scores_right = edge_sum[i+33: i+37]

            if max(edge_scores_left) \
                >= OW.KILLFEED_ICON_EDGE_HEIGHT_RATIO_LEFT[self.game_type] \
                and max(edge_scores_right) \
                >= OW.KILLFEED_ICON_EDGE_HEIGHT_RATIO_RIGHT[self.game_type]:
                edge_validation.append(True)
            else:
                edge_validation.append(False)
        edge_validation.extend([False]*6)

        return edge_validation

    def _set_player_info(self, player, position):
        """Set team & player name info for a matching result.

        Author:
            Appcell

        Args:
            None

        Returns:
            A dict of player info, with the form of:
            {
                "chara": "empty",   # name of chara, or "empty"
                "player": "empty",  # name of player, or "empty"
                "team": "empty",    # name of team, or "empty"
                "pos": -1,          # x-axis position of icon in killfeed
                                      row image
            }

        """
        res = {
            'chara': player['chara'], 
            'team': 'empty', 
            'player': 'empty',
            'pos': player['pos']}
        color_pos = OW.get_killfeed_team_color_pos(
            player['pos'], position)[self.game_type]

        color = self.image[color_pos[0], color_pos[1]]
        colors_ref = {}
        if self.frame.game.team_colors is not None:
            colors_ref = self.frame.game.team_colors
        else:
            colors_ref = self.frame.get_team_colors()
        dist_left = ImageUtils.color_distance(
            color, colors_ref['left'])
        dist_right = ImageUtils.color_distance(
            color, colors_ref['right'])

        if dist_left > OW.KILLFEED_MAX_COLOR_DISTANCE[self.game_type] \
            and dist_right > OW.KILLFEED_MAX_COLOR_DISTANCE[self.game_type]:
            res['pos'] = -1
            # cv2.imshow('t',self.image)
            # cv2.waitKey(0)
            # print [player['chara'], dist_left, dist_right, color, colors_ref['left'], colors_ref['right']]
            return res

        if dist_left < dist_right:
            res['team'] = self.frame.game.team_names['left']
        else:
            res['team'] = self.frame.game.team_names['right']

        chara = OW.get_chara_name(player['chara'])

        if res['team'] == self.frame.game.team_names['left']:
            res['player'] = next((item.name for item in self.frame.players[
                0:6] if item.chara == chara), "empty")
        else:
            res['player'] = next((item.name for item in self.frame.players[
                6:12] if item.chara == chara), "empty")

        return res

    def _set_assist_info(self, assist):
        """Set team & player name info for a assisting chara.

        Author:
            Appcell

        Args:
            None

        Returns:
            A dict of player info, with the form of:
            {
                "chara": "empty",   # name of chara, or "empty"
                "player": "empty",  # name of player, or "empty"
                "team": "empty",    # name of team, or "empty"
            }

        """
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
        """Get icon comparison scores of row image and icon references.

        Use match template in cv2 to get possible icon and their weights in the
        killfeed image.

        Author:
            Leavebody

        Args:
            edge_validation: A list of booleans. Should be the result of
                _validate_edge()

        Returns:
            A list of dict of matching results, including all possible icons 
            in this killfeed image. A matching result is in the form of:
            {
                "chara": "empty",   # name of chara, or "empty"
                "prob": "empty",  # score from comparison
                "pos": "empty",    # x-axis position of icon in killfeed
                                     row image
            }

        """
        result = []
        for (chara, icon) in self.frame.game.killfeed_icons_ref.iteritems():
            match_result = cv2.matchTemplate(
                self.image, icon, cv2.TM_CCOEFF_NORMED)

            # Find two most possible location of this character's icon in the killfeed image.
            # Mask the pixels around the first location to find the second one.
            _, max_val, _, max_loc = cv2.minMaxLoc(match_result)

            # Here we have to allow some error
            if sum(edge_validation[max_loc[0]-2: max_loc[0]+2]) > 0 \
                and max_val > OW.KILLFEED_MAX_PROB[self.game_type]:
                result.append({
                    'chara': chara,
                    'prob': max_val,
                    'pos': max_loc[0]
                })

            half_mask_width = 5
            mask_index_left = max((max_loc[0] - half_mask_width, 0))
            mask_index_right = min((
                max_loc[0] + half_mask_width + 1,
                OW.KILLFEED_WIDTH[self.game_type] - OW.KILLFEED_ICON_WIDTH[self.game_type]))
            match_result_masked = np.matrix(match_result)
            match_result_masked[0:match_result_masked.shape[
                0], mask_index_left: mask_index_right] = -1

            _, max_val2, _, max_loc2 = cv2.minMaxLoc(match_result_masked)

            if sum(edge_validation[max_loc2[0]-2: max_loc2[0]+2]) > 0 \
                and max_val2 > OW.KILLFEED_MAX_PROB[self.game_type]:
                result.append({
                    'chara': chara,
                    'prob': max_val2,
                    'pos': max_loc2[0]
                })

        return result

    def get_ability_and_assists(self):
        """Retrieve info of ability and assisting players in a row

        If distance between 2 avatar icons, width of arrow icon removed, is
        not divisible by width of an assist icon, then an ability icon must
        exist somewhere. Cut it off and compare with all possible ability
        icons to find the best match.

        After removing ability icon & arrow icon, what's left between 2
        avatars must be n assist icons. Cut each from killfeed image, and then
        compare with references. Pick the one with maximum score as result.

        All results are written into self.ability and self.assists.

        Author:
            Appcell

        Args:
            None

        Returns:
            None

        """
        if self.player1['pos'] == -1 or self.player2['pos'] == -1:
            return

        distance = self.player2[
            'pos'] - self.player1['pos'] - OW.KILLFEED_ICON_WIDTH[self.game_type]
        gap = ImageUtils.crop(
            self.image_with_gap,
            [0, self.image_with_gap.shape[0], self.player1['pos'], distance])

        ability_icon = ImageUtils.crop(
            self.image_with_gap,
            OW.get_ability_icon_pos(self.player2['pos'])[self.game_type])

        # Error gets too much with lowQ videos. Use edge detection instead.
        # Honestly it's not the best choice, since for non-OWL videos it 
        # doesn't work anymore. But again, for non-OWL videos we expect a 
        # better resolution.

        edge_image = cv2.Canny(self.image, 100, 200)

        # Get the "spanned" edge image.
        roi_x_min = self.player1['pos'] + OW.KILLFEED_ICON_WIDTH[self.game_type] + 4
        roi_x_max = self.player2['pos'] - OW.ABILITY_GAP_NORMAL[self.game_type]

        if roi_x_max - roi_x_min < OW.ASSIST_GAP[self.game_type]:
            return

        edge_span = (np.sum(edge_image, 0) / 255)[roi_x_min:roi_x_max]
        edges = list(filter(
            lambda i: edge_span[i] >= self.image.shape[0] * 0.7, 
            range(0, roi_x_max - roi_x_min)))
        if not edges:
            # Assist avatar doesn't exist
            return
        edge = edges[-1]  # The end of assist avatars list
        
        assist_num = int(round(float(edge) / OW.ASSIST_GAP[self.game_type]))
        ability_list = OW.ABILITY_LIST[self.player1['chara']]
        ability_icons_ref = self.frame.game.ability_icons_ref[
            self.player1['chara']]

        if (distance - OW.ABILITY_GAP_NORMAL[self.game_type]) % OW.ASSIST_GAP[self.game_type] > 5:
            # Has ability icon
            max_prob = -10
            for (ind, ability_index) in enumerate(ability_list):
                filtered_icon = self._preprocess_ability_icon(ability_icon)
                score = measure.compare_ssim(
                    filtered_icon, 
                    ability_icons_ref[ind], 
                    multichannel=True)
                if score > max_prob:
                    max_prob = score
                    self.ability = ability_index

            if max_prob < 0.1 and self.player1['chara'] == OW.GENJI:
                self.ability = OW.ABILITY_E

        for i in range(assist_num):
            # TODO: write this into ow.py!
            assist_icon = ImageUtils.crop(
                self.image,
                [
                    OW.ABILITY_ICON_Y_MIN[self.game_type],
                    OW.ASSIST_ICON_HEIGHT[self.game_type],
                    8 + self.player1['pos'] + i * OW.ASSIST_GAP[self.game_type] \
                        + OW.KILLFEED_ICON_WIDTH[self.game_type],
                    OW.ASSIST_ICON_WIDTH[self.game_type]])
            assist = {
                "chara": "empty",
                "player": "empty",
                "team": self.player1['team']
            }
            max_score = -10
            for (chara, icon) in self.frame.game.assist_icons_ref.iteritems():
                score = measure.compare_ssim(assist_icon, 
                                             icon, multichannel=True)
                if score > max_score:
                    max_score = score
                    assist['chara'] = chara

            self.assists.append(self._set_assist_info(assist))

    def _preprocess_ability_icon(self, icon):
        """Preprocess an ability icon cut from frame.

        Main idea here is to find color of icon first. Color of ability
        icon is same as of arrow icon on right side. Given color, remove all parts
        with different colors.

        Author:
            Appcell

        Args:
            None

        Returns:
            None

        """       
        ability_pos = OW.get_ability_icon_pos(self.player2['pos'])[self.game_type]
        color = self.image_with_gap[ability_pos[
            0] + ability_pos[1]/2, ability_pos[2] + ability_pos[3] + 6]
        filtered_icon = np.zeros((icon.shape[0], icon.shape[1]))
        
        # TODO: Labelling needed here!!! Especially when background looks
        # similar to foreground.

        # TODO: There must be a better way for this
        for i in range(icon.shape[0]):
            for j in range(icon.shape[1]):
                if ImageUtils.color_distance(icon[i, j, :], color) \
                    < OW.ABILITY_ICON_COLOR_FILTER_THRESHOLD[self.game_type]:
                    filtered_icon[i, j] = 255
        return filtered_icon.astype('uint8')

    def get_headshot(self):
        """Tell if elimination comes with a headshot.

        Author:
            Appcell

        Args:
            None

        Returns:
            None

        """ 
        ability_pos = OW.get_ability_icon_pos(self.player2['pos'])[self.game_type]
        color = self.image_with_gap[ability_pos[
            0] + ability_pos[1]/2, ability_pos[2] + ability_pos[3] + 6]

        # TODO: Write consts here into ow.py
        if ImageUtils.color_distance(color, np.array([255, 255, 255])) > 40:
            self.is_headshot = True
