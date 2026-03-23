import { createBrowserRouter } from "react-router-dom"
import Home from "../pages/Home"
import CpuDetails from "../pages/CpuDetails"
import Processes from "../pages/Processes"

const Router = createBrowserRouter([
    {
        path: "/",
        element: <Home />
    },
    {
        path: "/cpu-details",
        element: <CpuDetails />
    },
    {
        path: "/processes",
        element: <Processes />
    }
])

export default Router