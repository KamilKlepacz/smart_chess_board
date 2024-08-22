//// Wrapper over FastLED library, simplifies usage and hides

#include <FastLED.h>
#include <stdint.h> /// for special uint tyoes like uint32_t

#ifndef LED_STRIP_H
#define LED_STRIP_H

template <uint8_t PIN>
class LedStrip
{
    /// handles adresing led's in led strip individually
    /// acts as glorified dynamic array wrapper

    /// led strip connector pin
    const uint8_t pin = PIN;
    /// number of individually adressed leds
    uint32_t no_leds;
    /// raw led array pointer
    CRGB *leds;

public:
    /// object constructor,
    /// by default all leds are set to black (no collor)
    /// @param no_leds number of individually adressed leds
    LedStrip(uint32_t no_leds)
    {
        SetNoLeds(no_leds);
        Fill(CRGB::Black);
    };
    /// destructor
    ~LedStrip() { delete[] leds; }
    /// sets specific led to given color
    /// @param position id of adressed led
    /// @param color new color of targetted led
    void Set(uint32_t position, const CRGB &color)
    {
        leds[position] = color;
    }

    /// [] operator, gives direct acces to specified led
    /// @param position id of adressed led
    /// @returns direct acces to led under the given position
    CRGB &operator[](const uint32_t position)
    {
        assert(position < Size());
        return leds[position];
    }
    /// forces led strip to update it's colors
    void Update()
    {
        FastLED.show();
    }
    /// changes color in every connected led to specified
    /// @param color new color of each led
    void Fill(const CRGB &color)
    {
        for (uint32_t i = 0; i < no_leds; i++)
            leds[i] = color;
    }
    /// changes color in every connected led to black
    void Clear()
    {
        Fill(CRGB::Black);
    }
    /// @return number of individually adressed leds,
    ///     in std library every list-like class,
    ///     uses "size" function to acces length of list
    uint32_t Size() { return GetNoLeds(); }
    /// @return led strip connector pin
    uint8_t GetPin() { return pin; }

    /// @return number of individually adressed leds
    uint32_t GetNoLeds() { return no_leds; }

    /// setter for noumber of addressed leds
    /// @param no_leds new noumber of leds
    /// @note no_leds does not need to match length of physical led strip
    void SetNoLeds(uint32_t no_leds)
    {
        delete[] leds;
        this->no_leds = no_leds;
        leds = new CRGB[no_leds];
        FastLED.addLeds<NEOPIXEL, PIN>(leds, no_leds); // GRB ordering is assumed
    }

    void TurnRainbowOnAnimation(uint32_t animation_speed)
    {
        Clear();
        for (uint32_t j = 0; j < Size(); j++)
        {
            Set(j, Rainbow(j, Size() + 1));
            Update();
            delay(animation_speed);
        }
    }
};
/// calculates color present in id point on the rainbow scale <0 to max_id>
CRGB Rainbow(unsigned id, unsigned max_id);

/// comapere two colors if the're equal retuen true else return false
bool IsEqual(const CRGB &color_a, const CRGB &color_b);

// CRGB FromBase16(const string &color)

#endif