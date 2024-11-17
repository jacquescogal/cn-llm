import React from 'react'

type HTMLElementModal = HTMLElement & {
    showModal: () => void;
    close: () => void;
  };

const Modal = (props: {modalId:string, reactNode:React.ReactNode, form: React.ReactNode, onClickModal?:()=>void}) => {
  return (
    <>
      <div onClick={() => {
          (document.getElementById(
            props.modalId
          ) as HTMLElementModal)!.showModal();
          if (props.onClickModal) props.onClickModal();
        }}>

    {props.reactNode}
        </div>
      <dialog id={props.modalId} className="modal">
        <div className="modal-box w-fit max-w-fit">
          <div className="bg-base-100 text-base-content rounded-lg h-[35rem] w-[50rem] flex flex-row">
            <form method="dialog">
              <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" >
                ✕
              </button>
            </form>
            {props.form}
          </div>
        </div>
        <form method="dialog" className="modal-backdrop">
          <button>close</button>
        </form>
      </dialog>
    </>
  )
}

export default Modal