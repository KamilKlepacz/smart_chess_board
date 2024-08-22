#include "LedStrip.h"
CRGB Rainbow(unsigned id, unsigned max_id)
{
    // sine wave algorithm
    // 3 parts
    // 1 :
    // r = cos(i) , g = sin(i), b =0
    // 2 :
    // r = 0 , g = cos(i), b = sin(x)
    // 3:
    // r = sin(i) , g = 0, b = cos(x)
    // every part is max_height / 3 translates into 0, PI/2

    // so for example in point 1/3 * max_height
    // r = cos(PI/2) = 0, g = sin(PI/2) = 1, b = 0
    char witch_third = id / (max_id / 3);

    double height_in_radians;
    switch (witch_third)
    {
    case 0:
        height_in_radians = id * M_PI / (max_id / 3) / 2;

        return CRGB(cos(height_in_radians) * 255, sin(height_in_radians) * 255,
                    0);
    case 1:
        id -= max_id / 3;
        height_in_radians = id * M_PI / (max_id / 3) / 2;
        return CRGB(0, cos(height_in_radians) * 255,
                    sin(height_in_radians) * 255);

    case 2:
        id -= 2 * max_id / 3;
        height_in_radians = id * M_PI / (max_id / 3) / 2;
        return CRGB(sin(height_in_radians) * 255, 0,
                    cos(height_in_radians) * 255);
    }

    return CRGB::Red;
}
bool IsEqual(const CRGB &color_a, const CRGB &color_b)
{
    if (color_a.r != color_b.r)
        return false;
    if (color_a.g != color_b.g)
        return false;
    if (color_a.b != color_b.b)
        return false;
    return true;
}
