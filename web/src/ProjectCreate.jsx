import React from "react";
import M from "materialize-css";

export default ({onCreate}) => {
  const [progress, setProgress] = React.useState(0);
  const [isUploading, setIsUploading] = React.useState(false);

  const didSelectFiles = ({ target: { files: filelist } }) => {
    setIsUploading(true);
    setProgress(0);
    const files = Array.from(filelist);
    const fileCount = files.length;

    Promise.all(
      files.map(async (file) => {
        const formData = new FormData();
        formData.set("mesh", file);
        const response = await fetch("/api/projects", { method: "POST", body: formData });
        setProgress(files.indexOf(file) + 1 / fileCount * 100)
        M.toast({html: `Project was created for ${file.name}`});
        return await response.json();
      })
    ).then(() => {
      setIsUploading(false);
      onCreate && onCreate();
    });
  };

  return (
    <form className="fixed-action-btn">
      <label className={`btn-floating btn-large red progress-${progress}`}>
        <i className={`large material-icons ${isUploading && "spin"}`}>{isUploading ? "refresh" : "cloud_upload"}</i>
        <input
          onChange={didSelectFiles}
          disabled={isUploading}
          multiple
          className="offscreen"
          type="file"
          name="mesh"
        />
      </label>
    </form>
  );
};
