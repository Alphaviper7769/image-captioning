import './App.css'
import { Route, Routes } from 'react-router-dom'
import Home from './components/Home'
import History from './components/History'
import Login from './components/Login'
import Register from './components/Register'

function App() {
  

  return (
    <>
      <Routes>
        <Route path='/' element={<Home/>} ></Route>
        <Route path='/history' element={<History/>} ></Route>
        <Route path='/login' element={<Login/>} ></Route>
        <Route path='/register' element={<Register/>} ></Route>
      </Routes>
    </>
  )
}

export default App
