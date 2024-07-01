import React, { useRef } from "react";

const Upload = () => {
  const formref = useRef(null);
  const handleImageUpload = () => {
    formref.current.click();
  };

  return (
    <div className=" flex items-center flex-wrap p-5 justify-between  max-w-screen-xl h-[90vh] m-auto rounded-md">
      <div className="image-part h-full flex flex-col gap-4 justify-center w-[35vw]">
        <div
          onClick={handleImageUpload}
          className=" w-full cursor-pointer h-[45vh] flex-col flex items-center justify-center rounded-md shadow-2xl bg-white"
        >
          <form
            action=""
            method=""
            encType="multipart/form-data"
            className="hidden"
          >
            <input ref={formref} type="file" />
          </form>
          <i className="ri-upload-cloud-2-fill text-[10vw] text-zinc-400"></i>
          <p className="text-center text-sm text-zinc-400">
            Click to Upload Image
          </p>
        </div>
        <div className="w-full  flex items-center justify-around p-3">
          <button className="px-8 py-3 bg-red-500 hover:bg-red-600 text-xs rounded-full text-white"><i class="ri-delete-bin-line"></i> Delete</button>
          <button className="px-8 py-3 bg-blue-500 hover:bg-blue-600 text-xs rounded-full text-white"><i class="ri-check-line"></i> Submit</button>
        </div>
      </div>
      <div className="caption-part w-1/2 h-full rounded-md">
        <h1 className="font-semibold text-2xl text-center p-2 mt-8">Captions</h1>
        <div className="mt-8  w-full flex flex-col gap-8 p-3">
          <div className="w-full h-14 flex items-center text-sm font-semibold bg-zinc-300 shadow-xl rounded-md px-4">
            <h1>Caption 1</h1>
          </div>
          <div className="w-full h-14 flex items-center text-sm font-semibold bg-zinc-300 shadow-xl rounded-md px-4">
            <h1>Caption 2</h1>
          </div>
          <div className="w-full h-14 flex items-center text-sm font-semibold bg-zinc-300 shadow-xl rounded-md px-4">
            <h1>Caption 3</h1>
          </div>
          <div className="w-full h-14 flex items-center text-sm font-semibold bg-zinc-300 shadow-xl rounded-md px-4">
            <h1>Caption 4</h1>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Upload;
