import logo from './logo.svg';
import './App.css';
import { ChakraProvider } from "@chakra-ui/react"
import { Button, ButtonGroup } from "@chakra-ui/react"
import { Textarea, Text } from "@chakra-ui/react"
import { Heading } from "@chakra-ui/react"
import { Stack, HStack, VStack } from "@chakra-ui/react"
import React, { useState, useEffect } from 'react';
import Card from "./Card.js"

function App() {
  //const [query, setQuery] = useState("No inputted query yet");
  const [text, setText] = useState("N/A")
  //const [predict, setPredict] = useState("N/A")
  const [receive, setRecieve] = useState("No inputted query yet")
  const [responseList, setResponseList] = useState([])
  
    /*useEffect(() => {
      fetch('/send').then(res => res.json()).then(data => {
        setPredict(data.prediction);
        setRecieve(data.receive);
      });
    }, []);*/

    function handleSubmit(e) {
      e.preventDefault();
      const data = {text};
      console.log(JSON.stringify(data));
      fetch('/predict', {
        method: 'POST',
        headers: {
          'Content-type': 'application/json',
        },
        body : JSON.stringify(data),
      }).then(res => res.json().then(data => {
        //setPredict(data.prediction);
        setRecieve(data.receive);
        setResponseList(data.data);
        //responseList.map(entry => { return <Card link={entry.link} prediction={entry.prediction} /> })
      }))
    }

  return (
    <ChakraProvider>
      <VStack spacing="25px">
      <Heading>
        Fake News Detector
      </Heading>
        <Textarea placeholder="Enter claim" onChange={event => setText(event.target.value)}/>
        <Button colorScheme="blue" onClick = {handleSubmit}>Submit</Button>
        <Text>Submitted query: {receive}</Text>
        <Heading>Predictions:</Heading>
        <VStack spacing="30px">{responseList.map((entry) => <Card title={entry.title} link={entry.link} prediction={entry.prediction} />)}</VStack>
      </VStack>
    </ChakraProvider>
  );
}


export default App;
