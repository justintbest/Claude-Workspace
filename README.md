# Revit Line Exporter

A pyRevit addon that exports selected lines from Revit to the bowl backend API as A-Lines, used to generate seating bowls.

## Setup

1. Drop the `RevitLineExporter.extension` folder into `%AppData%\pyRevit\Extensions`
2. Fill in your credentials in `RevitLineExporter.extension/config.json`
3. Reload pyRevit — a **RevitLineExporter** tab will appear in the ribbon

## Usage

1. Select one or more connected straight lines in Revit (e.g. all 4 sides of a rectangle)
2. Click **Send Line** in the RevitLineExporter tab
3. Enter a name for the A-Line
4. The lines are chained into ordered points and POSTed to the backend
