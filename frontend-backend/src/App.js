import logo from './logo.svg';
import './App.css';
import { ChakraProvider } from "@chakra-ui/react"
import { Button, ButtonGroup } from "@chakra-ui/react"
import { Textarea, Text } from "@chakra-ui/react"
import { Heading } from "@chakra-ui/react"
import { Stack, HStack, VStack } from "@chakra-ui/react"
import React, { useState, useEffect } from 'react';

function App() {
  //const [query, setQuery] = useState("No inputted query yet");
  const [text, setText] = useState("")
  const [predict, setPredict] = useState("N/A")
  
    useEffect(() => {
      fetch('/send').then(res => res.json()).then(data => {
        setPredict(data.prediction);
      });
    }, []);

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
      })
      window.location.reload();
    }

  return (
    <ChakraProvider>
      <VStack spacing="50px">
      <Heading>
        Fake News Detector
      </Heading>
        <Textarea placeholder="Enter claim" onChange={event => setText(event.target.value)}/>
        <Button colorScheme="blue" onClick = {handleSubmit}>Submit</Button>
        <Text>Submitted query: {text}</Text>
        <Text>Prediction: {predict}</Text>
      </VStack>
    </ChakraProvider>
  );
}


export default App;
