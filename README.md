# Display-o-Tron and Envirophat Script

I have a Raspberry Pi ZeroW with a PhatStack attached with the above 2 modules attached to that.

I also have 3 other sensors attached to the provided analog connectors (MQ9 & MQ135). 
Then a CCS811 sensor board attached via the I2C protocol using the headers provided on the Display-o-Tron.

For more information see my blog post regarding the setup.

## CCS811

This is connected to the headers on the Display-o-Tron which provides access to the I2c interface. Its relatively easy using the AdaFruit CCS811 Python library
to get the values required for this.

## MQ9 & MQ135

These sensors connected via the analog inputs detect carbon monoxide (MQ9) and air quality (MQ135) but the 
sensors are quite difficult to use as a source for gathering PPM values but are good for getting 'alarm' levels.

Although alarm levels are not programmed into this script it would be relatively easy.

## Test Data

Thi data was gathered after following a tutorial online for getting a PPM value from MQ sensors but since reading the datasheets and other sources the chance of this is low.

## SystemD Setup File
You will notice a systemd file which can be used to enable this as a service which will start on boot and be accessible via systemctl.

## Todos

* Seperate the display and the environment sensors so the two could be used as extendable modules on top of the existing Pimoroni modules (This would be useful for people with the same setup but both boards are now obsolete so this may not happen)
* Create unit tests to ensure reliability of code.
* Create a CO alarm using the MQ9 sensor.
* Create an air quality alarm with the MQ135 sensor.
* Investigate why the CCS811 temperature and the BMP280 temperature on the Envirophat are so different from each other (4C).
* Complete blog post explaining setup with photos and 
