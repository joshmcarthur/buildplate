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

const VariantMetadata = ({variant}) => (
  <dl>
    <dt>Width (mm)</dt>
    <dd>{variant.metadata.size && Math.round(variant.metadata.size[0])}</dd>

    <dt>Height (mm)</dt>
    <dd>{variant.metadata.size && Math.round(variant.metadata.size[1])}</dd>

    <dt>Depth (mm)</dt>
    <dd>{variant.metadata.size && Math.round(variant.metadata.size[2])}</dd>

    <dt>Volume (mm^3)</dt>
    <dd>{variant.metadata.volume && Math.round(variant.metadata.volume)}</dd>
  </dl>
);

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
      <span className="card-title activator">
        {project.name}
        <i className="material-icons right">more_vert</i>
      </span>
    </div>
    <div class="card-action">
      <a href="#">View</a>
    </div>
    <div className="card-reveal">
      <span className="card-title">
        {project.name}
        <i className="material-icons right">close</i>
      </span>
      <p>
        <VariantMetadata variant={project.variants[project.variants.length - 1]} />
      </p>
    </div>
  </div>
);
