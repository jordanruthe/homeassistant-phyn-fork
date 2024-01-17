# homeassistant-phyn

Home Assistant custom component for interfacing with [Phyn](https://www.phyn.com) Smart Water Assistant and Kohler H2Wise+ by Phyn.

This integration currently provides the following capabilities:

- Daily water usage (compatible with Energy dashboard)
- Average water temperature, pressure, and flow (realtime not available)
- Shutoff valve control
- Away mode control

# Installation via HACS

This custom component can be integrated into [HACS](https://github.com/hacs/integration), so you can track future updates. If you have do not have have HACS installed, please see [their installation guide](https://hacs.xyz/docs/installation/manual).

1. Select HACS from the left-hand navigation menu.

2. Click _Integrations_.

3. Click the three dots in the upper right-hand corner and select _Custom Repositories_.

4. Paste "https://github.com/jordanruthe/homeassistant-phyn" into _Repository_, select "Integration" as _Category_, and click Add.

5. Close the Custom repositories dialog after it updates with the new integration.

6. "Phyn Smart Water Assistant" will appear in your list of repositories. Click to open, click the following Download buttons.

# Configuration

Configuration is done via the UI. Add the "Phyn" integration via the Integration settings, then provide the Phyn username and password in the configuration dialog.

## Changelog

_2023.01.00_

- Initial release

_2023.08.00_

- Added away mode control
