import React from 'react';
import {ScrollView, Text, TouchableOpacity} from 'react-native';
import styled from 'styled-components/native';

export const Home = function Home(): JSX.Element {
  return (
    <ScrollView>
      <StyledTouchableOpacity>
        <Text>Take a photo</Text>
      </StyledTouchableOpacity>
      <TouchableOpacity>
        <Text>Upload a photo</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

const StyledTouchableOpacity = styled.TouchableOpacity`
  background-color: red;
`;
