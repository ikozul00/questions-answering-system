import React from 'react';
import styled, {useTheme} from 'styled-components/native';
import {PictureButton} from './PictureButton';

export const Home = function Home(): JSX.Element {
  const theme = useTheme();

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
