import React, { useRef, useState } from "react";

const Upload = () => {
  const formref = useRef(null);
  const handleImageUpload = () => {
    formref.current.click();
  };

  const [image, setImage] = useState(null);
  const [imageUrl, setImageUrl] = useState('');
  const [image_id,setImage_id] = useState(null);
  const [caption1,setCaption1] = useState(null);
  const [caption2,setCaption2] = useState(null);

  const handleImageUploadChange = async(e) => {
    e.preventDefault();
    const file = e.target.files[0];
    setImage(file);
    const reader = new FileReader();
    reader.onload = () => {
      const imageDataUrl = reader.result;
      setImageUrl(imageDataUrl);
    };
    reader.readAsDataURL(file);
      const formData = new FormData();
      formData.append("image", e.target.files[0]);

      try {
        const response = await fetch(`http://127.0.0.1:5000/upload`, {
          method: "POST",
          body: formData,
        }).then(response => response.json()).then((data)=>setImage_id(data.file_id));

        
      } catch (error) {
        console.error("Error:", error);
      }
  };

  const removeImage = (e) => {
    e.preventDefault();
    setImage(null);
    setCaption1(null);
    setCaption2(null);
  };

  const handleImageSubmit = async(e) => {
    e.preventDefault();

    let caption=null;
    const predictEnglish  = await fetch(`http://127.0.0.1:5000/predict_caption/${image_id}`)
    .then((response) => response.json())
    .then((data) =>{
      setCaption1(data.caption)
      caption=data.caption;
    })

    const predictHindi  = await fetch(`http://127.0.0.1:5000/translate/${caption}`)
    .then((response) => response.json())
    .then((data) => setCaption2(data.caption))

  };

  return (
    <div className=" flex items-center flex-wrap p-3 justify-around  max-w-screen-xl  h-[90vh] m-auto rounded-md">
      <div className="image-part  h-full flex flex-col gap-3 justify-center w-1/2">
        {image == null ? (
          <div
            onClick={handleImageUpload}
            className=" w-full cursor-pointer h-[45vh] p-4 flex-col flex items-center justify-center rounded-md shadow-2xl bg-white"
          >
            <i className="ri-upload-cloud-2-fill text-[10vw] text-zinc-400"></i>
            <p className="text-center text-sm text-zinc-400">
              Click to Upload Image
            </p>
          </div>
        ) : (
          <div className=" w-full cursor-pointer h-[45vh] p-4 flex-col flex items-center justify-center rounded-md shadow-2xl bg-white">
            <div className="w-full h-full  rounded-sm">
              <img className="w-full h-full object-contain" src={imageUrl} alt="" />
            </div>
          </div>
        )}
        <form>
          <input
            ref={formref}
            onChange={handleImageUploadChange}
            className="hidden"
            type="file"
          />
          <div className="w-full  flex items-center justify-around p-3">
            <button
              onClick={removeImage}
              className="px-8 py-3 bg-red-500 hover:bg-red-600 text-xs rounded-full text-white"
            >
              <i className="ri-delete-bin-line"></i> Delete
            </button>
            <button
              onClick={handleImageSubmit}
              className="px-8 py-3 bg-blue-500 hover:bg-blue-600 text-xs rounded-full text-white"
            >
              <i className="ri-check-line"></i> Submit
            </button>
          </div>
        </form>
      </div>
      <div className="caption-part pt-20   w-1/3 h-full rounded-md">
        <h1 className="font-semibold text-2xl text-center p-2 mt-8">
          Caption
        </h1>
        <div className="mt-8  w-full flex flex-col gap-8 p-3">
          {caption1!=null?<div className="w-full h-14 flex items-center text-sm font-semibold bg-zinc-300 shadow-xl rounded-md px-4">
            <h1>{caption1.replace("startseq","").replace("endseq","")}</h1>
          </div>:<div className="w-full h-14 flex items-center text-sm font-semibold bg-zinc-300 shadow-xl rounded-md px-4">
          <h1>Please submit the file</h1>
          </div>}
          {caption2!=null?<div className="w-full h-14 flex items-center text-sm font-semibold bg-zinc-300 shadow-xl rounded-md px-4">
            <h1>{caption2.replace("startseq","").replace("endseq","")}</h1>
          </div>:<div className="w-full h-14 flex items-center text-sm font-semibold bg-zinc-300 shadow-xl rounded-md px-4">
          <h1>Please submit the file</h1>
          </div>}
          
        </div>
      </div>
    </div>
  );
};

export default Upload;
