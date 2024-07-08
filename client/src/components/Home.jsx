import React, { useEffect } from 'react'
import Navbar from './Navbar'
import Upload from './Upload'
import { useNavigate } from 'react-router-dom'

const Home = () => {

  const navigate = useNavigate();

  return (
    <div className="w-full h-screen bg-zinc-200">
        <Navbar/>
        <Upload/>
    </div>
  )
}

export default Home
