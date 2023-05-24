import React from 'react';
import styled from 'styled-components/native';
import {useNavigation} from '@react-navigation/native';
import type {HomeScreenNavigationProp} from '../navigation/types';
import {PictureButton} from './PictureButton';

export const Home = function Home(): JSX.Element {
  const navigation = useNavigation<HomeScreenNavigationProp>();

  return (
    <StyledScrollView
      contentContainerStyle={{
        flexGrow: 1,
        justifyContent: 'center',
      }}>
      <StyledViewContainer>
        <PictureButton type="capture" />
        <PictureButton type="library" />
        <StyledTouchableOpacity onPress={() => navigation.navigate('Results')}>
          <StyledTextLabel>Results</StyledTextLabel>
        </StyledTouchableOpacity>
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
  border-radius: ${({theme}) => theme.borderRadius};
`;

const StyledTextLabel = styled.Text`
  color: ${({theme}) => theme.colors.tertiary};
  font-size: ${({theme}) => theme.fontSizes.extralarge};
  text-align: center;
`;
