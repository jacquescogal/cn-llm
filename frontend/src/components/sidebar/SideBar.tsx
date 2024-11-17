import React from "react";
import { BiEdit } from "react-icons/bi";
import { HiMiniPencil } from "react-icons/hi2";
import { MdChat, MdMenuBook, MdSearch } from "react-icons/md";
import { RiRobot2Fill } from "react-icons/ri";
import { useLocation } from "react-router-dom";

interface navItem {
  name: string;
  icon: React.ReactNode;
  link?: string;
  children?: navItem[];
}

const SideBar = () => {
  const location = useLocation();
  const sideBarNavItems: navItem[] = [
    {
      name: "Explore",
      icon: <MdSearch />,
      link: "/explore",
    },
    {
      name: "Collection",
      icon: <MdMenuBook />,
      children: [
        {
          name: "View/Edit",
          icon: <BiEdit />,
          link: "/collection",
        },
        {
          name: "Review",
          icon: <HiMiniPencil />,
          link: "/review-due",
        },
      ],
    },
    {
      name: "AI",
      icon: <RiRobot2Fill />,
      children: [
        {
          name: "Chat",
          icon: <MdChat />,
          link: "/chat",
        }
      ],
    },
  ];
  return (
      <div className="w-56 bg-inherit flex justify-center p-2">
        <ul className="menu bg-base-100 shadow-md w-full m-4 rounded-xl text-base-content">
          {
            sideBarNavItems.map((item, index) => (
              <MenuItem key={index} item={item} currentLocation={location.pathname}/>
            ))
          }
        </ul>
      </div>
  );
};

const MenuItem = ({ item, currentLocation }: { item: navItem, currentLocation: string }) => {
  return (
    <li>
    {
      item.children ? <>
      <details open>
        <summary>{item.icon}{item.name}</summary>
        <ul>
          {item.children.map((child, index) => (
            <MenuItem key={index} item={child} currentLocation={currentLocation}/>
          ))}
        </ul>
      </details>
      </> : currentLocation === item.link?<a className="bg-black text-white hover:bg-black">{item.icon}{item.name}</a>:<a href={item.link}>{item.icon}{item.name}</a>
}</li>
  );
}

export default SideBar;
