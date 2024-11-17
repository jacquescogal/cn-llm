import React from 'react'
import SideBar from './sidebar/SideBar'
import { Outlet } from 'react-router-dom'

const Base = () => {
  return (
    <div className='absolute flex flex-row w-screen h-screen top-0 left-0 bg-slate-400'>
    <SideBar/>
    <div className="h-full w-full flex-1 overflow-y-scroll p-2">
    <Outlet/>
    </div>
    </div>
  )
}

export default Base