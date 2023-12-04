import './sidebar.scss'
import DashboardIcon from '@mui/icons-material/Dashboard';
import Inventory2Icon from '@mui/icons-material/Inventory2';
import ProductionQuantityLimitsIcon from '@mui/icons-material/ProductionQuantityLimits';
import QueryStatsIcon from '@mui/icons-material/QueryStats';
import NotificationsIcon from '@mui/icons-material/Notifications';
import PsychologyIcon from '@mui/icons-material/Psychology';
import SettingsIcon from '@mui/icons-material/Settings';
import PersonIcon from '@mui/icons-material/Person';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import { useNavigate  } from "react-router-dom";




function Sidebar() {
  let navigate = useNavigate(); 
  const routeChange = () =>{ 
    let path = `/signup`; 
    navigate(path);
  }
  return (
    <div className = "top2">
      <div className='sidebar'>
          <div className='center'>
            <ul>
              <p className="title">MAIN MENU</p>
              <li>
                <DashboardIcon className='icon' />
                <span>Dashboard</span>
              </li>
              <p className="title">LISTS MENU</p>
              <li>
                <Inventory2Icon className='icon' />
                <span>Products</span>
              </li>
              <li>
                <ProductionQuantityLimitsIcon className='icon' />
                <span>Machines</span>
              </li>
              <p className="title">OTHER MENU</p>
              <li>
                <QueryStatsIcon className='icon' />
                <span>Status</span>
              </li>
              <li>
                <NotificationsIcon className='icon' />
                <span>Notifications</span>
              </li>
              <p className="title">SERVICES</p>
              <li>
                <PsychologyIcon className='icon' />
                <span>Logs</span>
              </li>
              <li>
                <SettingsIcon className='icon' />
                <span>Settings</span>
              </li>
              <p className="title">ACCOUNT</p>
              <li onClick={routeChange}>
                <ExitToAppIcon className='icon' />
                <span>Logout</span>
              </li>
            </ul>
          </div>
      </div>
    </div>
   
  )
}

export default Sidebar