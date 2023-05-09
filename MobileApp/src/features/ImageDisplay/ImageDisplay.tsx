import React from 'react';
import {ScrollView, Text} from 'react-native';
import styled, {useTheme} from 'styled-components/native';

export const ImageDisplay = function Home(): JSX.Element {
  const theme = useTheme();

  return (
    <ScrollView
      contentContainerStyle={{
        flexGrow: 1,
        justifyContent: 'center',
      }}>
      <Text>Message</Text>
    </ScrollView>
  );
};
