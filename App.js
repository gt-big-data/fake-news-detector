import logo from './logo.svg';
import './App.css';
import { ChakraProvider } from "@chakra-ui/react"
import { Button, ButtonGroup } from "@chakra-ui/react"
import { Textarea } from "@chakra-ui/react"
import { Heading } from "@chakra-ui/react"
import { Stack, HStack, VStack } from "@chakra-ui/react"

function App() {
  return (
    <ChakraProvider>
      <VStack spacing="50px">
      <Heading>
        Fake News Detector
      </Heading>
        <Textarea placeholder="Enter claim" />
        <Button colorScheme="blue">Submit</Button>
      </VStack>
    </ChakraProvider>
  );
}

export default App;
