import cv2
import numpy as np
from operator import itemgetter
from skimage import measure
from . import overwatch as OW
from .utils import image as ImageUtils
import math

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
                     "player": -1,
                     "team": -1
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
            "chara": "empty",
            "player": -1,
            "team": -1,
            "pos": -1
        }
        self.player2 = {
            "chara": "empty",
            "player": -1,
            "team": -1,
            "pos": -1
        }
        self.ability = 0
        self.assists = []
        self.index = index
        self.is_valid = True
        self.is_headshot = False
        self.frame = frame
        self.game_type = frame.game_type
        self.game_version = frame.game_version

        killfeed_pos = OW.get_killfeed_pos(index, self.game_type, self.game_version)
        killfeed_with_gap_pos = OW.get_killfeed_with_gap_pos(index, self.game_type, self.game_version)
        self.image = ImageUtils.crop(frame.image, killfeed_pos)
        self.image_with_gap = ImageUtils.crop(
            frame.image, killfeed_with_gap_pos)

        self.get_players()
        self.get_ability_and_assists()
        self.get_headshot()

        # cv2.imshow('t', self.image)
        # cv2.waitKey(0)
        # print(self.player1["chara"])
        # print(self.player2["chara"])
        # print("Assists:")
        # for x in self.assists:
        #     print(x["chara"])
        # print("Abilities:")
        # print(self.ability)
        # print("======")
        self.free()

    def __eq__(self, other):
        if self.player1['chara'] == other.player1['chara'] \
                and self.player2['chara'] == other.player2['chara'] \
                and self.player1['team'] == other.player1['team'] \
                and self.player2['team'] == other.player2['team']:
            return True
        return False

    def free(self):
        """Free RAM by removing images from the Frame instance.

        Done after analysis.

        Author:
            Appcell

        Args:
            None

        Returns:
            None 
        """
        del self.image
        del self.image_with_gap

    def get_players(self):
        """Get 1 (or 2) player(s) info in a killfeed row. ONLY FOR OWL!!!

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

        # Differentiate results from 2 sides first, or it gets seriously wrong
        mean_pos = np.mean([i['pos'] for i in icons_weights])
        icons_weights_left = [i for i in icons_weights if i['pos'] < mean_pos]
        icons_weights_right = [i for i in icons_weights if i['pos'] >= mean_pos]
        mean_pos_left = np.mean([i['pos'] for i in icons_weights_left])
        mean_pos_right = np.mean([i['pos'] for i in icons_weights_right])


        if mean_pos_right < OW.get_ui_variable("KILLFEED_WIDTH", self.game_type, self.game_version) \
                - OW.get_ui_variable("KILLFEED_RIGHT_WIDTH", self.game_type, self.game_version):
            self.is_valid = False
            return
        if len(icons_weights) == 1 and mean_pos_right \
            >= OW.get_ui_variable("KILLFEED_WIDTH", self.game_type, self.game_version) \
            - OW.get_ui_variable("KILLFEED_RIGHT_WIDTH", self.game_type, self.game_version):
            # Only one icon exists
            if icons_weights and icons_weights[0]['pos'] \
                >= OW.get_ui_variable("KILLFEED_WIDTH", self.game_type, self.game_version) \
                - OW.get_ui_variable("KILLFEED_RIGHT_WIDTH", self.game_type, self.game_version):
                self.player2 = self._set_player_info(
                    icons_weights[0], OW.RIGHT, edge_validation)

        if abs(mean_pos_right - mean_pos_left) \
                < OW.get_ui_variable("KILLFEED_ICON_WIDTH", self.game_type, self.game_version) - 7:
            # Only one icon exists
            matched = icons_weights
            if matched and matched[0]['pos'] \
                    >= OW.get_ui_variable("KILLFEED_WIDTH", self.game_type, self.game_version) \
                    - OW.get_ui_variable("KILLFEED_RIGHT_WIDTH", self.game_type, self.game_version):
                self.player2 = self._set_player_info(
                    matched[0], OW.RIGHT, edge_validation)
        else:
            # 2 icons got recognized
            icons_weights_left = sorted(
                icons_weights_left, key=itemgetter('prob'), reverse=True)[0:2]
            icons_weights_right = sorted(
                icons_weights_right, key=itemgetter('prob'), reverse=True)[0:2]
            if icons_weights_left:
                self.player1 = self._set_player_info(
                    icons_weights_left[0], OW.LEFT, edge_validation)
            if icons_weights_right:
                self.player2 = self._set_player_info(
                    icons_weights_right[0], OW.RIGHT, edge_validation)

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
            Leavebody

        Args:
            None

        Returns:
            A list of boolean, result[i] is True if there can be a icon 
            starting from x=i, and result[i] is false if x=i can starts
            an icon.
        """
        edge_span = self._get_spanned_edge_image()

        # Sum on y axis and normalize
        edge_sum = edge_span.astype(
            'float') / OW.get_ui_variable("KILLFEED_ICON_HEIGHT", self.game_type, self.game_version)
        edge_validation = [False, False]
        for i in range(2, OW.get_ui_variable("KILLFEED_WIDTH", self.game_type, self.game_version) - 38):
            edge_scores_left = edge_sum[i-2: i+2]
            edge_scores_right = edge_sum[i+33: i+37]
            if max(edge_scores_left) \
                >= OW.get_ui_variable("KILLFEED_ICON_EDGE_HEIGHT_RATIO_LEFT", self.game_type, self.game_version) \
                and max(edge_scores_right)\
                >= OW.get_ui_variable("KILLFEED_ICON_EDGE_HEIGHT_RATIO_RIGHT", self.game_type, self.game_version):
                edge_validation.append(True)
            else:
                edge_validation.append(False)
        edge_validation.extend([False]*6)

        return edge_validation

    def _get_spanned_edge_image(self):
        edge_span = []
        if self.game_type == OW.GAMETYPE_OWL:
            # Generate edged image for this killfeed row.
            edge_image = cv2.Canny(self.image, 100, 200)
            # Get the "spanned" edge image.
            edge_span = (edge_image.sum(0) + np.roll(edge_image.sum(0), 1))/255
        elif self.game_type == OW.GAMETYPE_CUSTOM:
            # Hmm this doesn't work as well as I expected. Thus we switch to the old one.
            # colors_ref = self.frame.get_team_colors()
            # edge_image_left = ImageUtils.filter_by(
            #     self.image, 
            #     colors_ref[0],
            #     OW.KILLFEED_EDGE_MAX_COLOR_DISTANCE", self.game_type, self.game_version))
            # edge_image_right = ImageUtils.filter_by(
            #     self.image, 
            #     colors_ref[1],
            #     OW.KILLFEED_EDGE_MAX_COLOR_DISTANCE", self.game_type, self.game_version))
            # edge_image = edge_image_left + edge_image_right
            # edge_image = edge_image > 0
            # edge_span = (edge_image.sum(0) + np.roll(edge_image.sum(0), 1))

            edge_image = cv2.Canny(self.image, 100, 200)
            # Get the "spanned" edge image.
            edge_span = (edge_image.sum(0) + np.roll(edge_image.sum(0), 1))/255

        return edge_span

    def _set_player_info(self, player, position, edge_validation):
        """Set team & player name info for a matching result.

        Author:
            Appcell

        Args:
            None

        Returns:
            A dict of player info, with the form of:
            {
                "chara": "empty",   # name of chara, or "empty"
                "player": -1,  # index of player, or -1
                "team": -1,    # index of team, or -1
                "pos": -1,          # x-axis position of icon in killfeed
                                      row image
            }
        """
        res = {
            'chara': player['chara'],
            'team': -1,
            'player': -1,
            'pos': player['pos']}

        color_pos = OW.get_killfeed_team_color_pos(
            player['pos'], position, self.game_type, self.game_version)
        color = self.image[color_pos[0], color_pos[1]]
        if self.game_type == OW.GAMETYPE_OWL:
            # For OWL games, player names appear with colored background. The
            # original approach is applicable.
            pass
        else:
            # For non-OWL games, there's no colored background. Simply picking
            # up colors at a given position doesn't meet our needs anymore, 
            # since CC doesn't always give an exact location. Another approach
            # is, using previous edge_validation result to get edge location.
            base_position = player['pos'];
            min_edge_location = 1000
            max_edge_location = 0
            for x in range(base_position - 4, base_position):
                if edge_validation[x] is True:
                    if x > max_edge_location:
                        max_edge_location = x
                    if x < min_edge_location:
                        min_edge_location = x
            x1 = math.floor((min_edge_location + max_edge_location) / 2)
            # Usually x1 is more accurate, thus can be used to adjust avatar
            # location. But for robustness, a certain sampling area is needed.
            if player['pos'] > x1:
                color_sum = [0, 0, 0]
                for i in range(x1, player['pos']):
                    color_sum = color_sum + self.image[color_pos[0], i]
                color = color_sum / (player['pos'] - x1)
            else:
                color = self.image[color_pos[0], x1]
            res['pos'] = x1

        colors_ref = self.frame.get_team_colors()
        dist_left = 1000000
        dist_right = 1000000

        dist_left = ImageUtils.color_distance(
            color, colors_ref[0])
        dist_right = ImageUtils.color_distance(
            color, colors_ref[1])

        if dist_left < dist_right:
            res['team'] = OW.LEFT
        else:
            res['team'] = OW.RIGHT
        chara = OW.get_chara_name(player['chara'])
        if res['team'] == OW.LEFT:
            res['player'] = next((item.index for item in self.frame.players[
                0:6] if item.chara == chara), -1)
        else:
            res['player'] = next((item.index for item in self.frame.players[
                6:12] if item.chara == chara), -1)
        return res

    def _set_assist_info(self, assist):
        """Set team & player info for a assisting chara.

        Author:
            Appcell

        Args:
            None

        Returns:
            A dict of player info, with the form of:
            {
                "chara": "empty",   # name of chara, or "empty"
                "player": -1,  # index of player, or -1
                "team": -1,    # index of team, or -1
            }
        """
        res = {
            'chara': assist['chara'],
            'player': -1,
            'team': assist['team']
        }

        if assist['team'] == self.frame.game.team_names[OW.LEFT]:
            res['player'] = next((item.index for item in self.frame.players[
                0:6] if item.chara == assist['chara']), -1)
        elif assist['team'] == self.frame.game.team_names[OW.RIGHT]:
            res['player'] = next((item.index for item in self.frame.players[
                6:12] if item.chara == assist['chara']), -1)
        return res

    def _get_icons_weights(self, edge_validation):
        """Get icon comparison scores of row image and icon references.

        Use match template in cv2 to get possible icon and their weights in the
        killfeed image.

        Author:
            Leavebody, Appcell

        Args:
            edge_validation: A list of booleans. Should be the result of
                _validate_edge()

        Returns:
            A list of dict of matching results, including all possible icons 
            in this killfeed image. A matching result is in the form of:
            {
                "chara": "empty",   # name of chara, or "empty"
                "prob": -1,  # score from comparison
                "pos": -1,    # x-axis position of icon in killfeed
                                     row image
            }
        """
        result = []
        for (chara, icon) in self.frame.game.killfeed_icons_ref.items():
            match_result = cv2.matchTemplate(
                self.image, icon, cv2.TM_CCOEFF_NORMED)
            # Find two most possible location of this character's icon in the killfeed image.
            # Mask the pixels around the first location to find the second one.
            _, max_val, _, max_loc = cv2.minMaxLoc(match_result)
            # Here we have to allow some error, thus comes +/- 2
            if sum(edge_validation[max_loc[0] - 2: max_loc[0] + 2]) > 0 \
                    and max_val > OW.get_ui_variable("KILLFEED_MAX_PROB", self.game_type, self.game_version):
                    # TODO: write this into ow.py
                temp_icon = ImageUtils.crop(
                    self.image, 
                    [3, icon.shape[0], max_loc[0], OW.get_ui_variable("KILLFEED_ICON_WIDTH", self.game_type, self.game_version)])
                score_ssim = measure.compare_ssim(temp_icon, icon,
                                                  multichannel=True)
                if score_ssim >= OW.get_ui_variable("KILLFEED_SSIM_THRESHOLD", self.game_type, self.game_version):
                    result.append({
                        'chara': chara,
                        'prob': max_val,
                        'pos': max_loc[0]
                    })
            half_mask_width = 5
            mask_index_left = max((max_loc[0] + half_mask_width \
                - OW.get_ui_variable("ABILITY_GAP_NORMAL", self.game_type, self.game_version) \
                - OW.get_ui_variable("KILLFEED_ICON_WIDTH", self.game_type, self.game_version), 0))
            mask_index_right = min((
                max_loc[0] - half_mask_width + 1 \
                + OW.get_ui_variable("ABILITY_GAP_NORMAL", self.game_type, self.game_version) \
                + OW.get_ui_variable("KILLFEED_ICON_WIDTH", self.game_type, self.game_version),
                OW.get_ui_variable("KILLFEED_WIDTH", self.game_type, self.game_version) \
                - OW.get_ui_variable("KILLFEED_ICON_WIDTH", self.game_type, self.game_version)))

            match_result_masked = np.matrix(match_result)
            match_result_masked[0:match_result_masked.shape[
                0], mask_index_left: mask_index_right] = -1
            _, max_val2, _, max_loc2 = cv2.minMaxLoc(match_result_masked)

            if sum(edge_validation[max_loc2[0]-2: max_loc2[0]+2]) > 0 \
                    and max_val2 > OW.get_ui_variable("KILLFEED_MAX_PROB", self.game_type, self.game_version):
                temp_icon2 = ImageUtils.crop(
                    self.image, 
                    [3, icon.shape[0], max_loc2[0], OW.get_ui_variable("KILLFEED_ICON_WIDTH", self.game_type, self.game_version)])
                score_ssim2 = measure.compare_ssim(temp_icon2, icon,
                                                   multichannel=True)
                if score_ssim2 >= OW.get_ui_variable("KILLFEED_SSIM_THRESHOLD", self.game_type, self.game_version):
                    result.append({
                        'chara': chara,
                        'prob': max_val2,
                        'pos': max_loc2[0]
                    })

        # Since there's often a 'fake' avatar appearing in the middle, here we
        # have to do some filtering. The idea is, if positions of recoged
        # avatars range largely, this kf usually comes with 2 avatars (killer
        # and killed player). A pair of 2 avatars have a minimum distance
        # requirement: distance >= ABILITY_GAP_NORMAL + OW.KILLFEED_ICON_WIDTH
        # Another possible error: tm takes assist icon as a full avatar. This
        # is a bit tricky and my solution is not really optimal. I directly
        # remove those far from left/right edges.
        min_pos = 1000
        max_pos = 0
        for chara in result:
            if chara['pos'] < min_pos:
                min_pos = chara['pos']
            if chara['pos'] > max_pos:
                max_pos = chara['pos']

        if len(result) < 2:
            return result

        # calculate distance between each pair of potential recogs, then
        # remove those which are never visited
        result_validation = [False] * len(result)
        if max_pos - min_pos \
            > OW.get_ui_variable("ABILITY_GAP_NORMAL", self.game_type, self.game_version) \
            + OW.get_ui_variable("KILLFEED_ICON_WIDTH", self.game_type, self.game_version) - 10:
            for ind1, chara1 in enumerate(result):
                for ind2, chara2 in enumerate(result):
                    if abs(chara1['pos'] - chara2['pos']) \
                        > OW.get_ui_variable("ABILITY_GAP_NORMAL", self.game_type, self.game_version) \
                        + OW.get_ui_variable("KILLFEED_ICON_WIDTH", self.game_type, self.game_version) - 10 \
                        or abs(chara1['pos'] - chara2['pos']) < 10:
                        result_validation[ind1] = True
                        result_validation[ind2] = True

        # If 2 charas, remove those far from left/right edges
        result_filtered = []
        for ind, val in enumerate(result_validation):
            if val is True and abs(result[ind]['pos'] - min_pos) < 15 \
                or abs(result[ind]['pos'] - max_pos) < 15:
                result_filtered.append(result[ind])

        return result_filtered

    def get_ability_and_assists(self):
        """Retrieve info of ability and assisting players in a row

        If distance between 2 avatar icons, width of arrow icon removed, is
        not divisible by width of an assist icon, then an ability icon must
        exist somewhere. Cut it off and compare with all possible ability
        icons to find the best match.

        After removing ability icon & arrow icon, what's left between 2
        avatars must be n assist icons. Cut each from killfeed image, then
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
        distance = self.player2['pos'] - self.player1['pos'] \
            - OW.get_ui_variable("KILLFEED_ICON_WIDTH", self.game_type, self.game_version)
        gap = ImageUtils.crop(
            self.image_with_gap,
            [0, self.image_with_gap.shape[0], 
            self.player1['pos'] + OW.get_ui_variable("KILLFEED_ICON_WIDTH", self.game_type, self.game_version), distance])

        # Abilities
        ability_icon = ImageUtils.crop(
            self.image_with_gap,
            OW.get_ability_icon_pos(self.player2['pos'], self.game_type, self.game_version))

        ability_list = OW.ABILITY_LIST[self.player1['chara']]
        ability_icons_ref = self.frame.game.ability_icons_ref[
            self.player1['chara']]

        if (distance - OW.get_ui_variable("ABILITY_GAP_NORMAL", self.game_type, self.game_version)) \
            % OW.get_ui_variable("ASSIST_GAP", self.game_type, self.game_version) > 5:
            # Ability icon exists
            score = -10
            filtered_icon = self._preprocess_ability_icon(ability_icon)
            for (ind, ability_index) in enumerate(ability_list):
                match_result = cv2.matchTemplate(
                    filtered_icon, ability_icons_ref[ind], cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(match_result)
                temp_result = ImageUtils.crop(
                                filtered_icon,
                                [max_loc[1], ability_icons_ref[ind].shape[0],
                                max_loc[0], ability_icons_ref[ind].shape[1]])
                ssim = measure.compare_ssim(
                    temp_result,
                    ability_icons_ref[ind],
                    multichannel=False)
                score_ssim = cv2.matchTemplate(temp_result, ability_icons_ref[ind],
                                          cv2.TM_CCOEFF_NORMED)
                _, score_ssim, _, _ = cv2.minMaxLoc(score_ssim)

                if score_ssim + max_val > score \
                and score_ssim + max_val > OW.get_ui_variable("ABILITY_SSIM_THRESHOLD", self.game_type, self.game_version):
                    score = score_ssim + max_val
                    self.ability = ability_index

            if score < OW.get_ui_variable("ABILITY_SSIM_THRESHOLD", self.game_type, self.game_version) \
                and self.player1['chara'] == OW.GENJI:
                self.ability = OW.ABILITY_E

        # Assists

        # Error gets too much with lowQ videos. Use edge detection instead.
        # Honestly it's not the best choice, since for non-OWL videos it
        # doesn't work anymore. But again, for non-OWL videos we expect a
        # better resolution.

        # Get the "spanned" edge image.
        edge_image = cv2.Canny(self.image, 300, 500)
        roi_x_min = self.player1['pos'] + \
            OW.get_ui_variable("KILLFEED_ICON_WIDTH", self.game_type, self.game_version) + 4
        roi_x_max = self.player2['pos'] - OW.get_ui_variable("ABILITY_GAP_NORMAL", self.game_type, self.game_version)

        # If no enough space for assist icons, then no assists
        if roi_x_max - roi_x_min < OW.get_ui_variable("ASSIST_GAP", self.game_type, self.game_version):
            return  

        edge_span = (np.sum(edge_image, 0) / 255)[roi_x_min:roi_x_max]
        edges = list(filter(
            lambda i: edge_span[i] >= self.image.shape[0] \
                * OW.get_ui_variable("ASSIST_ICON_EDGE_HEIGHT_RATIO_LEFT", self.game_type, self.game_version),
            range(0, roi_x_max - roi_x_min)))

        # If no edges exist, then assist avatar doesn't exist, thus no assists
        print(edges)
        if not edges:
            return
        edge = edges[-1]
        
        assist_num = int(round(float(edge) / OW.get_ui_variable("ASSIST_GAP", self.game_type, self.game_version)))

        for i in range(assist_num):
            # TODO: write this into ow.py!
            assist_icon = ImageUtils.crop(
                self.image,
                OW.get_assist_icon_pos(self.player1['pos'], i, self.game_type, self.game_version))
            assist = {
                "chara": "empty",
                "player": -1,
                "team": self.player1['team']
            }
            max_score = -10
            for (chara, icon) in self.frame.game.assist_icons_ref.items():
                score = measure.compare_ssim(
                    assist_icon,
                    icon, 
                    multichannel=True)
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
        ability_pos = OW.get_ability_icon_pos(
            self.player2['pos'], self.game_type, self.game_version)

        color = self.image_with_gap[int(ability_pos[
                    0] + ability_pos[1]/2), ability_pos[2] + ability_pos[3] - 2]
        filtered_icon = np.zeros((icon.shape[0], icon.shape[1]))

        # TODO: Labelling needed here!!! Especially when background is
        # similar to foreground.
        # TODO: There must be a better way for this
        for i in range(icon.shape[0]):
            for j in range(icon.shape[1]):
                if ImageUtils.color_distance(icon[i, j, :], color) \
                        < OW.get_ui_variable("ABILITY_ICON_COLOR_FILTER_THRESHOLD", self.game_type, self.game_version):
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
        if self.player2['pos'] == -1:
            return
        ability_pos = OW.get_ability_icon_pos(
            self.player2['pos'], self.game_type, self.game_version)
        ability_icon = ImageUtils.crop(
            self.image_with_gap,
            ability_pos)
        color = self.image_with_gap[int(ability_pos[0] + ability_pos[1]/2), 
                ability_pos[2] + ability_pos[3] + 2]

        # TODO: Write consts here into ow.py
        if ImageUtils.color_distance(color, np.array([255, 255, 255])) \
            > OW.get_ui_variable("IS_HEADSHOT_COLOR_DISTANCE_THRESHOLD", self.game_type, self.game_version):
            self.is_headshot = True

    def dict(self):
        d = {
            'player1': self.player1,
            'player2': self.player2,
            'ability': self.ability,
            'is_headshot': self.is_headshot,
            'assists': self.assists,
        }
        return d
