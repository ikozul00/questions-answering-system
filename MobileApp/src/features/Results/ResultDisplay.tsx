import React, {useEffect, useState, useCallback} from 'react';
import styled from 'styled-components/native';
import {useRoute} from '@react-navigation/native';
import type {ResultScreenRouteProp} from '../navigation/types';

interface Question {
  pitanje: string;
  odgovor: string;
}

interface Data {
  id: string;
  title: string;
  image: string;
  answers: Question[];
}

export const ResultDisplay = function (): JSX.Element {
  const route = useRoute<ResultScreenRouteProp>();
  const [data, setData] = useState<Data>();
  const id = route.params.id;

  const loadData = useCallback(async () => {
    try {
      //Address of localhost on android emulator: 10.0.2.2
      const response = await fetch(
        `http://localhost:8000/getTaskData?id=${id}`,
      );
      if (!response.ok) {
        console.warn('Problem fetching text.');
        return;
      }
      const jsonRes = await response.json();
      if (jsonRes.id === "Id doesn't exist") {
        setData({id: '', title: '', image: '', answers: []});
        return;
      }
      setData({...jsonRes, answers: JSON.parse(jsonRes.answers)});
    } catch (err) {
      console.warn(err);
    }
  }, [route.params.id]);

  useEffect(() => {
    loadData();
  }, [route.params.id]);

  return (
    <StyledScrollView
      contentContainerStyle={{
        flexGrow: 1,
      }}>
      {data?.title && <StyledTextTitle>{data?.title}</StyledTextTitle>}
      {data?.image && (
        <StyledImage
          resizeMode="contain"
          source={{
            uri: `data:image/png;base64,${data?.image}`,
          }}
        />
      )}
      <StyledViewContainer>
        {data &&
          data.answers &&
          Object.keys(data.answers).map(i => (
            <StyledViewQuestion>
              <StyledTextQuestion>
                {i}. {data.answers[i].pitanje}
              </StyledTextQuestion>
              <StyledTextAnswer>{data.answers[i].odgovor}</StyledTextAnswer>
            </StyledViewQuestion>
          ))}
      </StyledViewContainer>
    </StyledScrollView>
  );
};

const StyledScrollView = styled.ScrollView`
  background-color: ${({theme}) => theme.colors.background};
  padding-top: ${({theme}) => theme.spaces.space16};
`;

const StyledImage = styled.Image`
  width: 90%;
  height: 400px;
  margin: 0 auto;
`;

const StyledViewContainer = styled.View`
  margin: ${({theme}) => theme.spaces.space16} auto;
`;

const StyledTextTitle = styled.Text`
  color: ${({theme}) => theme.colors.primary};
  font-size: ${({theme}) => theme.fontSizes.extralarge};
  text-align: center;
  margin-bottom: ${({theme}) => theme.spaces.space16};
`;

const StyledTextQuestion = styled.Text`
  font-size: ${({theme}) => theme.fontSizes.medium};
  font-weight: 700;
  color: ${({theme}) => theme.colors.secondary};
`;

const StyledTextAnswer = styled.Text`
  font-size: ${({theme}) => theme.fontSizes.medium};
  color: ${({theme}) => theme.colors.secondary};
`;

const StyledViewQuestion = styled.View`
  margin-bottom: ${({theme}) => theme.spaces.space8};
  width: 90%;
`;
