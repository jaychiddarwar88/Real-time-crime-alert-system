/* eslint-disable react/jsx-props-no-spreading */
import GitHubIcon from '@material-ui/icons/GitHub'
import LinkedInIcon from '@material-ui/icons/LinkedIn'
import { useEffect, useState } from 'react'
import { about } from '../../portfolio'
import './About.css'

const About = () => {
  const { name, role, description, resume, social } = about
  const [username, setUsername] = useState('')
  const [data, setData] = useState()
  const [buttonName, setButtonName] = useState('Click to Register')
  const [show, setShow] = useState(false)

  const url = 'https://crimealert.ml/uploader'

  const onButtonClick = () => {
    setButtonName('Registered Successfully!')
    setShow(true)
    fetch(url, {
      method: 'POST',
      body: data,
    })
      .then((res) => res.json())
      .then((res) => console.log('success', res))
  }

  const onUpload = (e) => {
    const { files } = e.target

    const x = new FormData()
    x.append('file', files[0])
    x.append('email', username)
    console.log(x.get('email'))
    setData(x)
  }

  return (
    <div className='about center'>
      {name && (
        <h1>
          <span className='about__name'>{name}</span>
        </h1>
      )}

      {role && <h2 className='about__role'>A {role}.</h2>}
      <p className='about__desc'>{description && description}</p>
      <input
        placeholder='Enter Email Address'
        type='email'
        onChange={(e) => {
          setUsername(e.target.value)
        }}
      />
      <div className='center upload'>
        <input onChange={onUpload} accept='.txt' type='file' />
      </div>
      <div className='about__contact center'>
        {social && (
          <>
            {social.github && (
              <a
                href={social.github}
                aria-label='github'
                className='link link--icon'
              >
                <GitHubIcon />
              </a>
            )}

            {social.linkedin && (
              <a
                href={social.linkedin}
                aria-label='linkedin'
                className='link link--icon'
              >
                <LinkedInIcon />
              </a>
            )}
          </>
        )}
      </div>
      <div className='center'>
        {username &&
          data &&
          /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(username) && (
            <button
              type='button'
              className='link link--icon'
              onClick={onButtonClick}
            >
              {buttonName}
            </button>
          )}
      </div>
      <div className='center'>
        {show && (
          <p className='about__para'>
            Our application will notify you via email if any of your friends are
            in danger. Stay safe.
          </p>
        )}
      </div>
    </div>
  )
}

export default About
