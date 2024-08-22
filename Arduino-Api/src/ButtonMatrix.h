/// Handles button pres detection
/// Can by multiplexing over provided connections
/// Library is Arduino specific
#include <stdint.h>
#include <assert.h>

#include <Arduino.h>

#ifndef BUTTON_MATRIX_H
#define BUTTON_MATRIX_H

struct PinState
{

    inline static uint8_t High = 1;
    inline static uint8_t Low = 0;
    static uint8_t Not(uint8_t state)
    {
        if (state == 0)
            return PinState::High;
        else
            return PinState::Low;
    }
};

class ButtonMatrix
{
public:
    // button matrix height (no_buttons in height)
    uint32_t height;
    // button matrix width (no_buttons in width), number of pins used as output
    uint32_t width;
    // pins used as outputs (array length must mach width parameter)
    uint8_t *power_pins_array;

    uint8_t analog_input_pin;
    // button current states, has length of height * width
    bool *button_matrix;

    uint32_t no_debouncer_measurements = 100;
    ButtonMatrix(const uint32_t height,
                 const uint32_t width,
                 uint8_t *power_pins_array,
                 const uint8_t analog_input_pin) : width(width), height(height), analog_input_pin(analog_input_pin)
    {
        /// constructs ButtonMatrix object, in main file should be constructed
        /// as global object
        /// @param width button matrix width (no_buttons in width)
        /// @param height button matrix height (no_buttons in height)
        /// @param power_pins_array pins used as outputs (array length must mach width parameter)

        /// @note passed pins must be addresable pins on your board

        this->power_pins_array = new uint8_t[width];
        for (uint32_t i = 0; i < width; i++)
            this->power_pins_array[i] = power_pins_array[i];

        button_matrix = new bool[width * height];
        for (uint32_t i = 0; i < width * height; i++)
            button_matrix[i] = false;
    };
    void Setup()
    {
        /// SEt up function should be invoked in the "setup()" function
        for (uint32_t w = 0; w < width; w++)
            pinMode(power_pins_array[w], OUTPUT);
    }
    uint32_t Scan()
    {
        /// scans buttons and updates button matrix field with new states
        /// this function might take a while to excute
        // uint32_t voltage = 0;
        // for (uint32_t i = 0; i < no_debouncer_measurements; i++)
        //     voltage += analogRead(analog_input_pin);

        return analogRead(analog_input_pin);
    }
    void DecodeVoltageMeasurement(uint32_t voltage)
    {
    }
    bool GetState(const uint32_t w, const uint32_t h)
    {
        return button_matrix[Conv1d(w, h)];
    }

    uint32_t GetHeight()
    {
        return height;
    }
    uint32_t GetWidth()
    {
        return width;
    }

    void SetStripStateHigh(const uint32_t w)
    {
        for (uint32_t i = 0; i < width; i++)
            digitalWrite(power_pins_array[w], LOW);
        digitalWrite(power_pins_array[w], HIGH);
    }
    uint32_t ReadStripState(const uint32_t w)
    {

        auto voltage = Scan();
        DecodeVoltageMeasurement(voltage);
        return voltage;
    }

    uint32_t Conv1d(const uint32_t h, const uint32_t w)
    {
        assert(h < height && w < width);
        return h * width + w;
    }
};

#endif