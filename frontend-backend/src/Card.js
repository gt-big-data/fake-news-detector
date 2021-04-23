import logo from './logo.svg';
import './App.css';
import { ChakraProvider } from "@chakra-ui/react"
import { Button, ButtonGroup } from "@chakra-ui/react"
import { Textarea, Text } from "@chakra-ui/react"
import { Heading, Link } from "@chakra-ui/react"
import { Stack, HStack, VStack, Box, Center} from "@chakra-ui/react"
import React, { useState, useEffect, Component} from 'react';

/*
<VStack spacing="5px" border="1px" borderColor="black">
          <Heading>
            Article: {this.props.link}
          </Heading>
          <Heading>
            Prediction: {this.props.prediction}
          </Heading>
          </VStack>
        </ChakraProvider>*/

class Card extends Component {
    render() {
      return (
        <ChakraProvider>
          <Center spacing="5px" border="1px" borderColor="green" h="300px">
          <VStack spacing="10px">
          <Heading>
            Article: <Link color="teal.500" href={this.props.link}>{this.props.title}</Link>
          </Heading>
          <Heading>
            Prediction: {this.props.prediction}
          </Heading>
          </VStack>
          </Center>
        </ChakraProvider>
      )
    }
}

export default Card
    