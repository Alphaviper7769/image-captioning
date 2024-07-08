import React from 'react'
import { useNavigate } from 'react-router-dom'

const Navbar = () => {
  const navigate = useNavigate()

  const History = () => {
    navigate('/history', { replace: true })
  }

  return (
    <div className='max-w-screen-xl h-[10vh] flex items-center justify-between px-10 m-auto  rounded-sm'>
      <h1 className='text-3xl'>Project</h1>
      <div className='flex items-center justify-between gap-10'>
        <h3 onClick={History} className='text-zinc-200 tracking-wide cursor-pointer px-6 py-2 font-semibold text-[0.8vw] rounded-full bg-blue-600'>History</h3>
      </div>
    </div>
  )
}

export default Navbar
