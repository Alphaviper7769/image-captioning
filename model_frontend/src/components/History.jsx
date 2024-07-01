import React from "react";
import HistoryCards from "./HistoryCards"
import { useNavigate } from "react-router-dom";

const History = () => {

    const navigate = useNavigate()

    const GotoHome = () => {
        navigate("/")
    }
  return (
    <div className="max-w-screen-xl min-h-screen bg-zinc-100 m-auto p-10">
      <h3 onClick={GotoHome}  className="hover:text-black cursor-pointer text-zinc-600 font-semibold">
        <i class="ri-arrow-left-line"></i> Go Back
      </h3>
      <div className="w-full  flex flex-col gap-4 pt-4">
        <HistoryCards/>
        <HistoryCards/>
        <HistoryCards/>
        <HistoryCards/>
      </div>
    </div>
  );
};

export default History;
