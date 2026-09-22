# Smart Urban Operations Platform

Welcome to the **Smart Urban Operations Platform** dashboard! This is a modern, responsive, and highly interactive Next.js application designed for city management, monitoring traffic, flood risks, hospital capacities, and emergency route planning.

## Features

- **Dynamic Layout**: A dark-themed, glassmorphic UI matching high-end CTO dashboard standards.
- **Client-Side Routing**: Fast, seamless transitions between sections (Traffic, Flood & Weather, Hospitals, etc.) using Next.js App Router.
- **Modular Components**: Built cleanly with Vanilla CSS Modules ensuring strict style boundaries and zero global collisions.
- **Mock Data Engine**: Powered by `src/lib/mockData.ts`, allowing you to easily swap out static data for real-time backend API calls.
- **Responsive Grid**: Widgets automatically adjust to screen width to ensure text remains readable on smaller monitors.

## Prerequisites

Before running the project locally, ensure you have the following installed:
- [Node.js](https://nodejs.org/en/) (Version 18+ recommended)
- `npm` (comes with Node.js)

## Getting Started

Follow these steps to get the project running on your local machine:

1. **Clone the repository** (if you haven't already)
   ```bash
   git clone <your-repo-url>
   cd "ai_twin city"
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **View the Application**
   Open your browser and navigate to [http://localhost:3000](http://localhost:3000). The dashboard should automatically load.

## Project Structure

- `src/app/`: Contains the Next.js routes (`/traffic`, `/hospitals`, etc.) and the root layout.
- `src/components/dashboard/`: Contains the core complex dashboard widgets (MapSection, LiveCityStatus, BottomWidgets).
- `src/components/layout/`: Contains the Sidebar and Header components.
- `src/components/ui/`: Reusable UI elements (Cards, Badges, Progress Bars).
- `src/lib/mockData.ts`: The central data store. Replace exports here with `fetch` calls to your API.

## Map Configuration (Optional)
Currently, the map section uses an elegant, styled placeholder to ensure the app builds cleanly out of the box without requiring third-party accounts. 

If you wish to integrate a real interactive map:
1. Obtain an API token from [Mapbox](https://www.mapbox.com/).
2. Re-install `react-map-gl` if it was removed (`npm install react-map-gl mapbox-gl`).
3. Add your token to a `.env.local` file at the root of the project:
   ```env
   NEXT_PUBLIC_MAPBOX_TOKEN=your_token_here
   ```
4. Update `src/components/dashboard/MapSection.tsx` to use the `react-map-gl` `Map` component.

## Contributing

Contributions are welcome! Please ensure any new components use their own `.module.css` file for styling and adhere to the existing dark-mode design system defined in `globals.css`.

## License
MIT License
