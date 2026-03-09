# CIP Frontend

The dashboard user interface for the Customer Intelligence Platform, built with React, TypeScript, and Vite. Features a **Light Premium UI** for high-end data visualization.

## Setup & Running

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```
   The dashboard will be available at `http://localhost:5173`.

3. **Build for Production**:
   ```bash
   npm run build
   ```

## Key Technologies
- **UI Framework**: React 19
- **Build Tool**: Vite 7
- **Styling**: Vanilla CSS with custom design tokens for Light Premium look.
- **Charts**: Recharts
- **Data Fetching**: TanStack React Query + Axios

## Dashboard Pages
- **Customer Health**: Holistic overview of portfolio scoring.
- **Churn Prediction**: High-risk identifies and distribution analysis.
- **CLV Analysis**: Breakdown of customer lifetime value percentiles.
- **Segmentation**: Persona-based customer categorization.
- **Retention Actions**: Logic-driven decisioning for customer incentives.
