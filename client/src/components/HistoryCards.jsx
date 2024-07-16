import React from 'react'

const HistoryCards = () => {
  return (
    <div className="w-full h-[45vh] flex items-center justify-between bg-zinc-300 rounded-md p-3">
          <div className="left-image shadow-lg w-[45%] rounded-lg h-full  overflow-hidden">
            <img
              src="https://images.unsplash.com/photo-1514477917009-389c76a86b68?q=80&w=1967&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
              alt=""
              className="w-full h-full object-cover"
            />
          </div>
          <div className="right-caption mt-10 w-[45%] flex flex-col gap-4 h-full">
            <div className="w-full h-14 flex items-center text-sm font-semibold bg-zinc-400 shadow-xl rounded-md px-4">
              <h1>Caption 1</h1>
            </div>
            <div className="w-full h-14 flex items-center text-sm font-semibold bg-zinc-400 shadow-xl rounded-md px-4">
              <h1>Caption 1</h1>
            </div>
            <div className="w-full h-14 flex items-center text-sm font-semibold bg-zinc-400 shadow-xl rounded-md px-4">
              <h1>Caption 1</h1>
            </div>
            <div className="w-full h-14 flex items-center text-sm font-semibold bg-zinc-400 shadow-xl rounded-md px-4">
              <h1>Caption 1</h1>
            </div>
          </div>
        </div>
  )
}

export default HistoryCards
