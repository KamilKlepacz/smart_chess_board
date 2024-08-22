#include "ButtonMatrix.h"
#include "LedStrip.h"
#include <String.h>

uint32_t ToDecimal(const String &color_str);
uint32_t HandleChar(const char c);
CRGB ParseColor(String color_str);

template <uint8_t PIN>
int HandleLedStripUpdate(String command, LedStrip<PIN> &led_strip_handle);

int HandleBoardScan(ButtonMatrix &button_matrix_handle);

template <uint8_t PIN>
void Parse(const String &command, LedStrip<PIN> &led_strip_handle, ButtonMatrix &button_matrix_handle)
{
    if (command.substring(0, 3) == "set")
    {
        HandleLedStripUpdate(command, led_strip_handle);
        Serial.write('\n');
    }
    else if (command.substring(0, 3) == "get")
    {
        HandleBoardScan(button_matrix_handle);
        Serial.write('\n');
    }
    else if (command.substring(0, 3) == "snc") // synchronize
    {
        HandleLedStripUpdate(command, led_strip_handle);
        HandleBoardScan(button_matrix_handle);
        Serial.write('\n');
    }
}

template <uint8_t PIN>
int HandleLedStripUpdate(String command, LedStrip<PIN> &led_strip_handle)
{
    command.remove(0, 3);
    led_strip_handle.Clear();
    String message = "";
    for (uint32_t i = 0; i < led_strip_handle.Size(); i++)
    {
        String color_str = command.substring(i * 7, i * 7 + 6);
        // message += color_str;
        // message += " ";
        CRGB color = ParseColor(color_str);
        // message += String((int)color[0]);
        // message += " ";
        // message += color.g;
        // message += " ";
        // message += color.g;
        // message += " ";
        uint32_t id = i;

        {
            int r = id / 8;
            int c = id % 8;

            if (r % 2 == 1)
                c = 7 - c;

            id = r * 8 + c;
        }
        led_strip_handle.Set(id, color);
    }

    led_strip_handle.Update();
    // Serial.write(message.c_str());
    Serial.write("ok");

    // Serial.write("GENERAL BUTTON MATRIX ERROR");

    return 0;
}

int HandleBoardScan(ButtonMatrix &button_matrix_handle)
{
    String answer = "";
    for (int16_t w = 0; w < button_matrix_handle.GetWidth(); w++)
    {
        answer += String(w) + ' ';
        button_matrix_handle.SetStripStateHigh(w);
        answer += String(button_matrix_handle.Scan());
        answer += ' ';
    }
    Serial.write("ok");
    Serial.write(answer.c_str());
    return 0;
}

CRGB ParseColor(String color_str)
{
    uint8_t r, g, b;
    // incoming data looks as follows:
    // e.g. e5g8ab
    // these are 3 256 bit numbers encoded in base 16 and passed together
    // if one og these is < 16 string would look like:
    // 01b700
    // always 6 characters long

    color_str.toUpperCase();
    // to prepate for base 16 to base 10 conversion
    r = ToDecimal(color_str.substring(0, 2));
    g = ToDecimal(color_str.substring(2, 4));
    b = ToDecimal(color_str.substring(4, 6));
    return CRGB(r, g, b);
}

uint32_t HandleChar(const char c)
{
    if (c >= '0' && c <= '9')
        return (int)c - '0';
    else
        return (int)c - 'A' + 10;
}

// Function to convert a number from base 16 to base 10
// to decimal
uint32_t ToDecimal(const String &color_str)
{
    int len = color_str.length();
    int power = 1; // Initialize power of base
    int num = 0;   // Initialize result
    int i;

    // Decimal equivalent is str[len-1]*1 +
    // str[len-2]*base + str[len-3]*(base^2) + ...
    for (i = len - 1; i >= 0; i--)
    {
        // A digit in input number must be
        // less than number's base
        if (HandleChar(color_str[i]) >= 16)
        {
            return -1;
        }

        num += HandleChar(color_str[i]) * power;
        power = power * 16;
    }

    return num;
}
