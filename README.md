# Analytics (Signal Processing)
This is the main analytics module. It serves as the "brain" of the arm in the sense that it analyzes EMG sensor data and the camera feed (eventually) to determine the best grip type and when to apply the grip.

## Installation
```bash
# Install poetry -- follow the instructions here: https://python-poetry.org/docs/#installation
# Clone the repository
git clone git@github.com:BEARUBC/analytics_module.git

# Run the following commands to initialize the `sgcp` submodule
git submodule init
git submodule update

# Install dependencies
cd <REPOSITORY>
poetry install

# Finally, start the analytics module
poetry run python -m analytics
```

## File Structure
```
analytics/
├─ adc/          -> Handles communication with ADC (MCP3008) over SPI
├─ common/       -> Common logging utilities and other useful methods
├─ configs/      -> Defines configurable properties for each module
├─ gpm/          -> Handles communication with GPM over TCP 
├─ metrics/      -> Exposes custom Prometheus endpoint for monitoring
├─ processing/   -> Processes incoming signals from the ADC
├─ protobuf/     -> Protobuf generated definitions
```


