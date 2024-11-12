import React from 'react'
import { FloatingBubble } from 'antd-mobile'
import { MessageFill } from 'antd-mobile-icons'

export function FloatingBubbleButton() {
  const onClick = () => {
    console.log("굳")
  }
  return (
    <div>
      <FloatingBubble
        style={{
          '--initial-position-bottom': '24px',
          '--initial-position-right': '24px',
          '--edge-distance': '24px',
        }}
        onClick={onClick}
      >
        <MessageFill fontSize={32} />
      </FloatingBubble>
    </div>
  )
};