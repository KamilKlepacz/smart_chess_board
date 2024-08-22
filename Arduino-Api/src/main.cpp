// Led strip example

// #include "LedStrip.h"

// LedStrip<5> led_strip(8);

// void setup()
// {
//   led_strip.Clear();

//   for (uint32_t j = 0; j < led_strip.Size(); j++)
//     led_strip.Set(j, CRGB::Beige);
//   led_strip.Update();
// }

// void loop()
// {
//   delay(1000);
// }

// Button matrix example
#include "ButtonMatrix.h"
#include <String.h>
#include "LedStrip.h"
#include "CommandParser.h"

LedStrip<11> led_strip(64);
uint8_t power_pins_array[] = {2, 4};
ButtonMatrix button_matrix((uint32_t)2, (uint32_t)2, &power_pins_array[0], A0);
void setup()
{
  led_strip.TurnRainbowOnAnimation(50);
  led_strip.Fill(CRGB::Green);
  led_strip.Update();
  button_matrix.Setup();
  Serial.begin(115200);
  Serial.write("ready\n");
}
void loop()
{
  String command = Serial.readStringUntil('\n');
  Parse(command, led_strip, button_matrix);
}
/*
#include <Arduino.h>
#include <String.h>
#include "LedStrip.h"
LedStrip<11> led_strip(8);
CRGB ParseColor(String color_str);

#include <String.h>

uint32_t HandleChar(const char c);
uint32_t ToDecimal(const String &color_str);

void setup()
{
  Serial.begin(115200);
  Serial.write("ready\n");
  led_strip.Fill(CRGB::Green);
  led_strip.Update();
}
void loop()
{
  if (Serial.available())
  {

    String message = Serial.readStringUntil('\n');
    if (message.substring(0, 3) == "set")
    {
      // set board colors
      message.remove(0, 3);
      for (uint32_t i = 0; i < led_strip.Size(); i++)
      {
        String color_str = message.substring(i * 7, 6);
        CRGB color = ParseColor(color_str);
        led_strip.Set(i, color);
      }
      led_strip.Update();
      // Serial.print(1);
      Serial.write("ok\n");
    }
    else if (message.substring(0, 3) == "get")
    {

      // set board state
      message.remove(0, 3);
      Serial.print(0);
      Serial.print('\n');
    }
    // Serial.print('\n');
  }
  else
  {

    button_matrix.Scan();
  }
  // Serial.print("ok\n");
}

*/