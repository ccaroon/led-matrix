import random

from my_wifi import MyWiFi
from chronos import Chronos
from lib.colors.basic import Basic as BasicColors
from info_panel.panel import Panel
import info_panel.iss.icons as Icons
from info_panel.iss.gps_area import GPSArea

class ISSPanel(Panel):
    UPDATE_INTERVAL = 10

    def __init__(self, x, y):
        super().__init__(x, y, BasicColors.palette())

        durham = GPSArea.from_file(
            "info_panel/iss/data/durham.coords", reverse=True
        )
        nc = GPSArea.from_file(
            "info_panel/iss/data/nc.coords", reverse=True
        )
        usa = GPSArea.from_file(
            "info_panel/iss/data/usa.coords", reverse=True
        )
        # NOTE: names here must match ICONS names
        self.__places = (
            {
                'name': "The USA",
                'color': BasicColors.get("white"),
                'area': usa
            },
            {
                'name': "North Carolina",
                'color': BasicColors.get("blue"),
                'area': nc
            },
            {
                'name': "Durham",
                'color': BasicColors.get("green"),
                'area': durham
            }
        )

    def __draw_icon(self, icon, color_map):
        for idx, pixel in enumerate(icon):
            self._bitmap[idx] = color_map[pixel]

    def _update_display(self):
        # Get ISS position
        resp = MyWiFi.REQUESTS.get("http://api.open-notify.org/iss-now.json")
        if resp.status_code == 200:
            data = resp.json()
            iss_coords = (
                float(data['iss_position']['latitude']),
                float(data['iss_position']['longitude'])
            )
            # Check list of places
            curr_place = None
            for place in self.__places:
                # print(f"Checking '{place['name']}' [{place['color']}]")
                if place['area'].contains(iss_coords):
                    curr_place = place

            # Display results
            if curr_place:
                self.__draw_icon(
                    Icons.ICONS.get(curr_place['name']),
                    (
                        self._palette.from_name("black"),
                        self._palette.from_color(curr_place['color']),
                        self._palette.from_color(curr_place['color']),
                    )
                )
                print(f"{Chronos.datetime_str()} - The ISS is currently over {curr_place['name']}.")
            else:
                self.__draw_icon(
                    Icons.ICONS.get("Earth"),
                    (
                        self._palette.from_name("black"),
                        self._palette.from_name("blue"),
                        self._palette.from_name("green"),
                        self._palette.from_name("white"),
                    )
                )
                iss_pt = random.randint(1, self._bitmap.width * self._bitmap.height)
                self._bitmap[iss_pt-1] = self._palette.from_name("white")

                # print("The ISS is NOT overhead right now.")
                # print(f"https://www.google.com/maps/search/{iss_coords[0]},+{iss_coords[1]}/@{iss_coords[0]},{iss_coords[1]},4z")
        else:
            msg = "Err"
            length = self._strlen(msg, spacing=1)
            center = self._find_center(length, 5)
            self._border(BasicColors.get("red"))
            self._draw_string(
                center[0], center[1],
                msg, BasicColors.get("red"),
                spacing=1
            )
            print(resp.content)














#
