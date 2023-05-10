import type {NativeStackNavigationProp} from '@react-navigation/native-stack';
import type {RouteProp} from '@react-navigation/native';

export type StackParamList = {
  Home: undefined;
  Image: {uri: string | undefined};
};

export type HomeScreenNavigationProp = NativeStackNavigationProp<
  StackParamList,
  'Image'
>;

export type ImageScreenRouteProp = RouteProp<StackParamList, 'Image'>;
