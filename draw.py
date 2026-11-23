#!/usr/bin/env python3
"""Render the 23 November 2026 front page as a 1024x1024 PNG.

Newspaper-style infographic: masthead, a lead climate story with a
cracked-globe drawing, four supporting stories in a grid, and a dark
"also today" strip at the bottom. Run: python3 draw.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(BASE, "entry.png")

CANVAS = (1024, 1024)
BG = (247, 243, 232)
FG = (20, 20, 20)
ACCENT = (176, 30, 36)
SEA = (29, 78, 137)
DARK = (16, 32, 54)
LEAF = (31, 110, 61)
AMBER = (212, 160, 23)
CARD = (255, 253, 245)
MUTED = (90, 86, 76)
TEXT = (48, 48, 48)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF_BOLD = FONT_DIR + "/LiberationSerif-Bold.ttf"
SERIF_REG = FONT_DIR + "/LiberationSerif-Regular.ttf"
SANS_BOLD = FONT_DIR + "/LiberationSans-Bold.ttf"
SANS_REG = FONT_DIR + "/LiberationSans-Regular.ttf"


class Sheet:
    def __init__(self):
        self.img = Image.new("RGB", CANVAS, BG)
        self.pen = ImageDraw.Draw(self.img)

    def typeface(self, path, size):
        return ImageFont.truetype(path, size)

    def split_lines(self, text, face, width):
        """Greedy wrap: longest prefix of words that still fits."""
        out = []
        current = ""
        for word in text.split():
            candidate = (current + " " + word).strip()
            if self.pen.textlength(candidate, font=face) <= width:
                current = candidate
            else:
                if current:
                    out.append(current)
                current = word
        if current:
            out.append(current)
        return out

    def write_block(self, x, y, text, face, color, width, gap):
        """Draw a wrapped paragraph; return the y below its last line."""
        for line in self.split_lines(text, face, width):
            self.pen.text((x, y), line, font=face, fill=color)
            y += gap
        return y

    def write_centred(self, x, y, text, face, color):
        self.pen.text((x, y), text, font=face, fill=color, anchor="ma")

    def hline(self, x0, x1, y, color, weight=2):
        self.pen.line([(x0, y), (x1, y)], fill=color, width=weight)

    def draw_masthead(self):
        self.write_centred(512, 12, "THE WORLD",
                           self.typeface(SERIF_BOLD, 84), FG)
        self.hline(28, 996, 116, FG, 3)
        self.write_centred(512, 126, "MONDAY  23  NOVEMBER  2026",
                           self.typeface(SANS_BOLD, 29), ACCENT)
        self.hline(28, 996, 170, ACCENT, 4)

    def draw_globe(self, cx, cy, r):
        self.pen.ellipse([cx - r, cy - r, cx + r, cy + r],
                         fill=(52, 120, 180), outline=DARK, width=4)
        for box, shade in [((cx - 78, cy - 62, cx - 8, cy - 6), (74, 148, 74)),
                           ((cx - 12, cy + 18, cx + 66, cy + 78), (74, 148, 74)),
                           ((cx + 30, cy - 70, cx + 84, cy - 18), (94, 164, 84))]:
            self.pen.ellipse(box, fill=shade)
        crack = [(cx - 52, cy - 88), (cx - 18, cy - 44), (cx - 44, cy - 6),
                 (cx - 2, cy + 34), (cx - 30, cy + 66), (cx + 6, cy + 96)]
        self.pen.line(crack, fill=ACCENT, width=7, joint="curve")
        sx, sy, sr = cx + 96, cy - 96, 26
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0),
                       (-0.7, -0.7), (0.7, 0.7), (-0.7, 0.7), (0.7, -0.7)]:
            self.pen.line([(sx + dx * (sr + 4), sy + dy * (sr + 4)),
                           (sx + dx * (sr + 14), sy + dy * (sr + 14))],
                          fill=AMBER, width=4)
        self.pen.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=AMBER,
                         outline=(176, 120, 10), width=3)

    def draw_lead(self):
        self.pen.text((28, 188), "CLIMATE  \u2022  LEAD STORY",
                      font=self.typeface(SANS_BOLD, 22), fill=ACCENT)
        self.pen.text((28, 216), "COP31 COLLAPSES",
                      font=self.typeface(SERIF_BOLD, 72), fill=FG)
        body = ("No deal in Turkey as talks run longest ever. 190+ nations fail "
                "to bridge the fossil-fuel and finance divide; the EU and island "
                "states reject a draft that omits fossil fuels \u2014 the first "
                "no-deal climate talks since 2009.")
        self.write_block(28, 306, body, self.typeface(SERIF_REG, 23),
                         TEXT, 600, 30)
        self.draw_globe(838, 322, 98)
        self.write_centred(838, 424, "2.8\u00b0C warming path",
                           self.typeface(SANS_BOLD, 22), ACCENT)

    def draw_card(self, x, y, w, h, tag, tag_color, title, body):
        self.pen.rectangle([x, y, x + w, y + h], fill=CARD,
                           outline=(200, 192, 170), width=2)
        self.pen.rectangle([x, y, x + 8, y + h], fill=tag_color)
        tx = x + 24
        self.pen.text((tx, y + 14), tag,
                      font=self.typeface(SANS_BOLD, 21), fill=tag_color)
        hy = y + 46
        face = self.typeface(SERIF_BOLD, 29)
        for line in self.split_lines(title, face, w - 46):
            self.pen.text((tx, hy), line, font=face, fill=FG)
            hy += 35
        self.write_block(tx, hy + 8, body, self.typeface(SANS_REG, 20),
                         TEXT, w - 46, 26)

    def draw_grid(self):
        stories = [
            ("IRAN WAR", ACCENT,
             "Trump wants a \u201creal deal\u201d as Iran strikes Bahrain",
             "Iran hits a civilian site in Bahrain \u2014 2 hurt \u2014 and says it "
             "struck US positions. At least 3 tankers attacked in the Strait of Hormuz."),
            ("UKRAINE", SEA,
             "Russian warship sunk off Libya",
             "Corvette Merkury capsizes in Benghazi after a suspected Ukrainian "
             "sea-drone attack. Zelenskyy confirms Kyiv did it. Dymer strike kills 11."),
            ("UNITED STATES", DARK,
             "Democrats win 258 seats \u2014 biggest House majority since 1992",
             "US lead over China in Asia shrinks to a record low: 78.9 to 73.6 on "
             "the Lowy Power Index \u2014 a gap of just 5.3 points."),
            ("TRADE", LEAF,
             "EU\u2013Indonesia sign landmark trade deal",
             "After a decade of talks: tariffs scrapped on 98.5% of EU goods, "
             "exporters save \u20ac600m+ a year, markets of 730 million people."),
        ]
        top, height, gap = 452, 208, 16
        width = (1024 - 2 * 28 - gap) // 2
        for i, (tag, color, title, body) in enumerate(stories):
            col, row = i % 2, i // 2
            self.draw_card(28 + col * (width + gap), top + row * (height + gap),
                           width, height, tag, color, title, body)

    def draw_ticker(self):
        top = 900
        self.pen.rectangle([0, top, 1024, 1024], fill=DARK)
        self.pen.text((28, top + 10), "ALSO TODAY",
                      font=self.typeface(SANS_BOLD, 21), fill=AMBER)
        light = (235, 235, 235)
        face = self.typeface(SANS_REG, 19)
        first = ("GAZA \u2014 Israeli strike on a truck kills 3  \u2022  POLAND \u2014 Russian "
                 "missiles and a drone violate airspace; NATO meets  \u2022  MEXICO \u2014 "
                 "Sinaloa cartel chief \u201cChapo Isidro\u201d captured")
        second = ("S. KOREA \u2014 Education minister quits over AI exam chaos  \u2022  "
                  "CONGO \u2014 Fighting disrupts Ebola response")
        y = self.write_block(28, top + 36, first, face, light, 1024 - 56, 23)
        self.write_block(28, y + 1, second, face, light, 1024 - 56, 23)
        self.write_centred(
            512, 1009,
            "Sources: BBC, Reuters, AP, CNN, NYT, WSJ, DW, Euronews, Lowy Institute",
            self.typeface(SANS_REG, 12), (160, 175, 195))

    def save(self):
        self.img.save(TARGET, "PNG", optimize=True)
        print("wrote", TARGET, os.path.getsize(TARGET), "bytes")


def main():
    page = Sheet()
    page.draw_masthead()
    page.draw_lead()
    page.draw_grid()
    page.draw_ticker()
    page.save()


if __name__ == "__main__":
    main()
