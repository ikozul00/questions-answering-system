import React, {useCallback} from 'react';
import type {PropsWithChildren} from 'react';
import {PermissionsAndroid} from 'react-native';
import styled, {useTheme} from 'styled-components/native';
import * as ImagePicker from 'react-native-image-picker';
import {useNavigation} from '@react-navigation/native';
import type {HomeScreenNavigationProp} from '../navigation/types';

type PictureButtonProps = PropsWithChildren<{
  type: string;
}>;

const requestCameraPermission = async () => {
  try {
    const status = await PermissionsAndroid.check(
      PermissionsAndroid.PERMISSIONS.CAMERA,
    );
    if (!status) {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.CAMERA,
      );
      if (granted === PermissionsAndroid.RESULTS.GRANTED) {
        console.log('You can use the camera');
        const status = await PermissionsAndroid.check(
          PermissionsAndroid.PERMISSIONS.WRITE_EXTERNAL_STORAGE,
        );
        if (!status) {
          const granted = await PermissionsAndroid.request(
            PermissionsAndroid.PERMISSIONS.WRITE_EXTERNAL_STORAGE,
          );
          if (granted === PermissionsAndroid.RESULTS.GRANTED) {
            console.log('You can use the storage');
            return true;
          } else {
            console.log('Storage permission denied');
            return false;
          }
        } else {
          return true;
        }
      } else {
        console.log('Camera permission denied');
        return false;
      }
    } else {
      return true;
    }
  } catch (err) {
    console.warn(err);
  }
};

export const PictureButton = function PictureButton({
  type,
}: PictureButtonProps): JSX.Element {
  const navigation = useNavigation<HomeScreenNavigationProp>();

  interface Action {
    title: string;
    type: 'capture' | 'library';
    options: ImagePicker.CameraOptions | ImagePicker.ImageLibraryOptions;
  }

  const cameraParams: Action = {
    title: 'Take Image',
    type: 'capture',
    options: {
      saveToPhotos: true,
      mediaType: 'photo',
      includeBase64: false,
    },
  };

  const galeryParams: Action = {
    title: 'Select Image',
    type: 'library',
    options: {
      mediaType: 'photo',
      includeBase64: false,
    },
  };

  const onButtonPress = useCallback(async (params: Action) => {
    let result;
    if (type === 'capture') {
      const isPermitted = await requestCameraPermission();
      if (isPermitted) {
        result = await ImagePicker.launchCamera(params.options);
      }
      console.log('Problem with permissions while taking a photo');
    } else {
      result = await ImagePicker.launchImageLibrary(params.options);
    }
    if (result?.assets) {
      const data = result.assets[0];
      navigation.navigate('Image', {
        file: {
          fileName: data.fileName,
          type: data.type,
          uri: data.uri,
        },
      });
      return;
    }
    console.log('Image not taken.');
  }, []);

  return (
    <StyledTouchableOpacity
      onPress={() =>
        onButtonPress(type === 'capture' ? cameraParams : galeryParams)
      }>
      <StyledTextLabel>
        {type === 'capture' ? 'Take a photo' : 'Upload a photo'}
      </StyledTextLabel>
    </StyledTouchableOpacity>
  );
};

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
