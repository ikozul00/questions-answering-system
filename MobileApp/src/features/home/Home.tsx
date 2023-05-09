import React, {useState, useCallback} from 'react';
import {PermissionsAndroid} from 'react-native';
import styled, {useTheme} from 'styled-components/native';
import * as ImagePicker from 'react-native-image-picker';
import {PictureButton} from './PictureButton';

export const Home = function Home(): JSX.Element {
  const theme = useTheme();
  const [response, setResponse] = useState<any>(null);

  return (
    <StyledScrollView
      contentContainerStyle={{
        flexGrow: 1,
        justifyContent: 'center',
      }}>
      <StyledViewContainer>
        <PictureButton type="capture" />
        <PictureButton type="library" />
      </StyledViewContainer>
    </StyledScrollView>
  );
};

const StyledScrollView = styled.ScrollView`
  background-color: ${({theme}) => theme.colors.background};
`;

const StyledViewContainer = styled.View`
  background-color: ${({theme}) => theme.colors.background};
  align-items: center;
  justify-content: space-around;
  gap: ${({theme}) => theme.spaces.space48};
`;

const StyledTouchableOpacity = styled.TouchableOpacity`
  background-color: ${({theme}) => theme.colors.secondary};
  padding-top: ${({theme}) => theme.spaces.space16};
  padding-bottom: ${({theme}) => theme.spaces.space16};
  width: 70%;
  border-radius: 10px;
`;

const StyledTextLabel = styled.Text`
  color: ${({theme}) => theme.colors.tertiary};
  font-size: ${({theme}) => theme.fontSizes.extralarge};
  text-align: center;
`;
