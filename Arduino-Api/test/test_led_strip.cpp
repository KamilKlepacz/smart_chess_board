#include "../src/LedStrip.h"

void test_led_strip()
{
    LedStrip<5> led_strip(10);
    for (uint32_t j = 0; j < led_strip.Size(); j++)
        if (!IsEqual(led_strip[j], CRGB::Black))
            printf("error in test_led_strip");
}

void main()
{
    test_led_strip();
}