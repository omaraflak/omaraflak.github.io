:title: HCT — Hue Chroma Tone
:description: Google's color system
:year: 2025
:month: 8
:day: 18

[](https://m3.material.io/blog/science-of-color-design)

Google's color system is called HCT:

- **Hue** is what we commonly think of as "color", it takes values in `[0, 360]`
- **Chroma** is how *vibrant* the color is, it takes values in `[0, 150]`
- **Tone** is the shade of the color, it takes values in `[0, 100]`

In the grid below, the horizontal axis represents variations of *tone*, while the vertical axis represents variations of *hue*. A tone of 0 is always black, and a tone of 100 is always white. When the *chroma* goes to zero it transforms all tones into shades of grey.

[#include](assets/hct/hct.html)

What's interesting with this color system is that it tries to be as **perceptually accurate** as possible: for a given hue and chroma, all tones *seem* to belong to the same family of colors. This makes it very easy to create a color palette starting with a seed color.

Another feature of HCT is that it is [accessible](https://developer.mozilla.org/en-US/docs/Web/Accessibility) (in this case, compatible with people with visual impairements): it guarantees that 2 colors picked 40-50 tones appart will always have high enough contrast, e.g. such that one could be a background color, and the other a text color on top of it.

# 3D

We can visualize those three components on a color wheel.

[#include](assets/hct/hct-3d.html)
