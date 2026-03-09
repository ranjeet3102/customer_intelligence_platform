import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";
import CustomerHealthPage from "../pages/CustomerHealthPage";
import ChurnPage from "../pages/ChurnPage";
import CLVPage from "../pages/CLVPage";
import SegmentationPage from "../pages/SegmentationPage";
import RetentionPage from "../pages/RetentionPage";

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<DashboardLayout />}>
                    <Route index element={<CustomerHealthPage />} />
                    <Route path="churn" element={<ChurnPage />} />
                    <Route path="clv" element={<CLVPage />} />
                    <Route path="segmentation" element={<SegmentationPage />} />
                    <Route path="retention" element={<RetentionPage />} />
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}
