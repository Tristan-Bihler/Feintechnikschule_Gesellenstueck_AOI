import Sidebar from './Sidebar'
import Navbar from './Navbar'


const Home = () => {
  return (
    <div className="home">
        <Sidebar />
        <div className="homeContainer">
        <Navbar />
          <div className='widgets'>

          </div>
          <div className="charts">

          </div>
        </div>
    </div>
    
  )
}

export default Home