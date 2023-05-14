import React, {useState} from 'react';
import {Text} from 'react-native';
import styled from 'styled-components/native';
import type {ImageScreenRouteProp} from '../navigation/types';
import {useRoute} from '@react-navigation/native';

export const ImageDisplay = function ImageDisplay(): JSX.Element {
  const route = useRoute<ImageScreenRouteProp>();
  const fileData = route.params.file;
  const [result, setResult] = useState('');

  const [name, setName] = useState('');

  const uploadFile = async () => {
    const data = new FormData();
    data.append('file', {
      uri: fileData.uri,
      name: fileData.fileName,
      type: fileData.type,
    });
    data.append('title', name);
    console.log('evo');
    try {
      //Address of localhost on android emulator: 10.0.2.2
      const response = await fetch(`http://localhost:8000/uploadImage/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        body: data,
      });
      if (!response.ok) {
        console.warn('Problem fetching text.');
        return;
      }
      const jsonRes = await response.json();
      console.log(jsonRes);
      setResult(jsonRes.result);
    } catch (err) {
      console.warn(err);
    }
  };

  return (
    <StyledScrollView
      contentContainerStyle={{
        flexGrow: 1,
      }}>
      <StyledViewContainer>
        <StyledViewInputContainer>
          <StyledTextLabel>Title:</StyledTextLabel>
          <StyledTextInput
            placeholder={'Some title'}
            value={name}
            onChangeText={value => setName(value)}
          />
        </StyledViewInputContainer>
        <StyledImage
          resizeMode="contain"
          source={{
            uri: fileData.uri,
          }}
        />
        <StyledTouchableOpacity onPress={uploadFile}>
          <StyledTextButtonLabel>Submit</StyledTextButtonLabel>
        </StyledTouchableOpacity>
        {result && <Text>{result}</Text>}
      </StyledViewContainer>
    </StyledScrollView>
  );
};

const StyledScrollView = styled.ScrollView`
  background-color: ${({theme}) => theme.colors.background};
`;

const StyledViewContainer = styled.View`
  align-items: center;
  padding-top: ${({theme}) => theme.spaces.space24};
`;

const StyledViewInputContainer = styled.View`
  width: 90%;
  flex-direction: row;
  gap: 10px;
  align-items: center;
  margin-bottom: ${({theme}) => theme.spaces.space24};
`;

const StyledImage = styled.Image`
  width: 90%;
  height: 400px;
`;

const StyledTextLabel = styled.Text`
  font-size: ${({theme}) => theme.fontSizes.large};
  font-weight: 500;
  color: black;
`;

const StyledTextInput = styled.TextInput`
  border-color: ${({theme}) => theme.colors.secondary};
  border-width: ${({theme}) => theme.spaces.space2};
  flex: 1;
  border-radius: ${({theme}) => theme.borderRadius};
  font-size: ${({theme}) => theme.fontSizes.medium};
  padding-left: ${({theme}) => theme.spaces.space8};
`;

//TODO: make this look like something
const StyledTouchableOpacity = styled.TouchableOpacity`
  background-color: ${({theme}) => theme.colors.secondary};
  margin-top: 20px;
  padding: 10px;
  border-radius: ${({theme}) => theme.borderRadius};
`;

//TODO: make this look like something
const StyledTextButtonLabel = styled.Text`
  color: ${({theme}) => theme.colors.tertiary};
  font-size: ${({theme}) => theme.fontSizes.medium};
  text-align: center;
`;
