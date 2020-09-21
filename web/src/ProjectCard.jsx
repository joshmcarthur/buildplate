import React from "react";
import defaultThumbnail from "./default-thumbnail.svg";

const thumbnailUrl = (project) => {
  if (!project.variants.length) return defaultThumbnail;
  const variant = project.variants[0];
  const card_image = project.variants[0].preview_image_paths.find((pi) => pi.type === "card_image");

  if (card_image) {
    return `/api/projects/${project.name}/${card_image.path}`
  } else 
  if (variant.preview_image_paths[0]) {
    return `/api/projects/${project.name}/${variant.preview_image_paths[0].path}`;
  } else {
    return defaultThumbnail;
  }
};

export default ({ project }) => (
  <div className="card medium">
    <div className="card-image waves-effect waves-block waves-light">
      <img
        className="activator"
        alt={`${project.name} preview`}
        src={thumbnailUrl(project)}
      />
    </div>
    <div className="card-content">
      <span className="card-title activator grey-text text-darken-4">
        {project.name}
        <i className="material-icons right">more_vert</i>
      </span>
      <p>
        <a href="#">View</a>
      </p>
    </div>
    <div className="card-reveal">
      <span className="card-title grey-text text-darken-4">
        {project.name}
        <i className="material-icons right">close</i>
      </span>
      <p>Here is some more information about this product that is only revealed once clicked on.</p>
    </div>
  </div>
);
