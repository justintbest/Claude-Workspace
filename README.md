# Revit Line Exporter

A pyRevit addon that sends a selected line from Revit to a REST API.

## Setup

1. Add this repo to your pyRevit extensions folder
2. Fill in `config.json` with your API endpoint and key
3. Reload pyRevit — a **RevitLineExporter** tab will appear in the ribbon

## Usage

1. Select a single straight line in Revit
2. Click **Send Line** in the RevitLineExporter tab
3. The line's start/end points are POSTed to your server as JSON

## Payload

```json
{
    "element_id": 123456,
    "start": {"x": 0.0, "y": 0.0, "z": 0.0},
    "end":   {"x": 10.0, "y": 0.0, "z": 0.0}
}
```
