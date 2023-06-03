import React from 'react';
import type {PropsWithChildren} from 'react';
import styled from 'styled-components/native';
import {useNavigation} from '@react-navigation/native';
import type {ResultsScreenNavigationProp} from '../navigation/types';

type ResultButtonProps = PropsWithChildren<{
  id: string;
  title: string;
}>;

export const ResultButton = function PictureButton({
  id,
  title,
}: ResultButtonProps): JSX.Element {
  const navigation = useNavigation<ResultsScreenNavigationProp>();

  return (
    <StyledTouchableOpacity
      onPress={() => navigation.navigate('ResultDisplay', {id: id})}>
      <StyledTextLabel>{title}</StyledTextLabel>
    </StyledTouchableOpacity>
  );
};

const StyledTouchableOpacity = styled.TouchableOpacity`
  padding-top: ${({theme}) => theme.spaces.space16};
`;

const StyledTextLabel = styled.Text`
  color: ${({theme}) => theme.colors.secondary};
  text-decoration: underline;
  font-size: ${({theme}) => theme.fontSizes.medium};
`;
