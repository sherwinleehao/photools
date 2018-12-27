#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Filmora PRo Titles

Author: Sherwin Lee

Website: Sherwinleehao.com

Last edited: 20181101
"""

import os, time, json, csv
import re, uuid, shutil
import cv2
import xmltodict
from PIL import Image

XML = '''<?xml version="1.0" encoding="UTF-8"?>
<BiffCompositeShot AppVersion="10.1.0000.00000" Version="1" AppEdition="2000"><Assets><MediaAsset Version="6"><ID>f69f51ab-2a8c-46ae-9e91-f4f29b736b86</ID><Name>Doodle Pack - Lowerthird 1.mp4</Name><ParentFolderID>00000000-0000-0000-0000-000000000000</ParentFolderID><IsImageSequence>0</IsImageSequence><HWAccelerate>1</HWAccelerate><MergedAudioFilename></MergedAudioFilename><MergedAudioOffset>0</MergedAudioOffset><OverrideFrameRate>0</OverrideFrameRate><FrameRate>30</FrameRate><OverridePAR>0</OverridePAR><PAR>0</PAR><OverrideAlpha>0</OverrideAlpha><AlphaMode>0</AlphaMode><OverrideColorLevels>0</OverrideColorLevels><ColorLevels>0</ColorLevels><InPoint>0</InPoint><OutPoint>124</OutPoint><Instances><Instance CompID="4fe99388-e1b0-415d-897f-87ba41e0ccb0" Type="2" ID="965d2514-208d-4d80-a0fb-2e1f7ba60074"/></Instances><Filename>Media\Doodle Pack - Lowerthird 1.mp4</Filename></MediaAsset><MediaAsset Version="6"><ID>a9a3772c-ce0a-43aa-8047-f93545b08132</ID><Name>Doodle Pack - Lowerthird 1_L0.mp4</Name><ParentFolderID>00000000-0000-0000-0000-000000000000</ParentFolderID><IsImageSequence>0</IsImageSequence><HWAccelerate>1</HWAccelerate><MergedAudioFilename></MergedAudioFilename><MergedAudioOffset>0</MergedAudioOffset><OverrideFrameRate>0</OverrideFrameRate><FrameRate>30</FrameRate><OverridePAR>0</OverridePAR><PAR>0</PAR><OverrideAlpha>0</OverrideAlpha><AlphaMode>0</AlphaMode><OverrideColorLevels>0</OverrideColorLevels><ColorLevels>0</ColorLevels><InPoint>-1</InPoint><OutPoint>-1</OutPoint><Instances><Instance CompID="4fe99388-e1b0-415d-897f-87ba41e0ccb0" Type="2" ID="bbf5795c-d0d2-4dcd-b829-1b3e8ae13ce5"/></Instances><Filename>Media\Doodle Pack - Lowerthird 1_L0.mp4</Filename></MediaAsset></Assets><CompositionAsset Version="15"><ID>4fe99388-e1b0-415d-897f-87ba41e0ccb0</ID><Name>Doodle Pack - Lowerthird 1</Name><ParentFolderID>00000000-0000-0000-0000-000000000000</ParentFolderID><CTI>23</CTI><InPoint>0</InPoint><OutPoint>125</OutPoint><TimelineZoom>0</TimelineZoom><SplitterPosition>424</SplitterPosition><TimelineTimeFormat>1000</TimelineTimeFormat><TimelineSnapMode>1000</TimelineSnapMode><AudioVideoSettings Version="1"><FrameCount>125</FrameCount><AudioSampleRate>48000</AudioSampleRate><Width>1920</Width><Height>1080</Height><PAR>0</PAR><PARCustom>1</PARCustom><FrameRate>25</FrameRate></AudioVideoSettings><RenderSettings Version="1"><FogEnabled>0</FogEnabled><FogNearDistance>900</FogNearDistance><FogFarDistance>2000</FogFarDistance><FogDensity>1</FogDensity><FogColor A="1" R="0" G="0" B="0"/><FogFalloff>0</FogFalloff><MotionBlurEnabled>1</MotionBlurEnabled><ShutterAngle>180</ShutterAngle><ShutterPhase>0</ShutterPhase><MaxNumOfSamples>20</MaxNumOfSamples><UseAdaptiveSamples>1</UseAdaptiveSamples></RenderSettings><Layers><TextLayer Version="12"><Dimensions>0</Dimensions><IncludeInDepthMap>1</IncludeInDepthMap><TextBox Version="0"><ID>d7f5de85-16fa-4105-a6de-1d7bc1bd50b0</ID><MinX>0</MinX><MaxX>491.641</MaxX><MinY>0</MinY><MaxY>162.578</MaxY><Mode>0</Mode><VerticalAlignment>2</VerticalAlignment><TopIndentation>0</TopIndentation><BottomIndentation>0</BottomIndentation><Tokens><Tk Jf="0" V="1" Tp="1" Sa="0" Sb="0" Li="0" ID="e829bb26-35b7-4c07-8239-879b6f517d3c" Fi="0" Ri="0"/><Tk V="1" Ft="e10c48c1-8978-49d3-bc4b-a4f90328c317" Tp="0" ID="362d8228-e9a9-485c-8c70-5935010b7a86" Ch="76"/><Tk V="1" Ft="e10c48c1-8978-49d3-bc4b-a4f90328c317" Tp="0" ID="c99a49f0-2dc6-482b-aefb-8aacdadfc557" Ch="111"/><Tk V="1" Ft="e10c48c1-8978-49d3-bc4b-a4f90328c317" Tp="0" ID="893542ed-cab1-4764-a853-8f6417b03797" Ch="119"/><Tk V="1" Ft="e10c48c1-8978-49d3-bc4b-a4f90328c317" Tp="0" ID="e0b3f4e6-f214-4f71-9455-e202fe7bfc55" Ch="101"/><Tk V="1" Ft="e10c48c1-8978-49d3-bc4b-a4f90328c317" Tp="0" ID="e251efb9-2eae-47f8-b11b-7c0d3c169a9f" Ch="114"/><Tk V="1" Ft="e10c48c1-8978-49d3-bc4b-a4f90328c317" Tp="0" ID="d592d41d-8094-4267-baba-d921f936b479" Ch="116"/><Tk V="1" Ft="e10c48c1-8978-49d3-bc4b-a4f90328c317" Tp="0" ID="0392a72d-eb92-46ac-afed-e55b0fd4e160" Ch="104"/><Tk V="1" Ft="e10c48c1-8978-49d3-bc4b-a4f90328c317" Tp="0" ID="99294db3-8190-4e08-8d08-dae39a6385b9" Ch="105"/><Tk V="1" Ft="e10c48c1-8978-49d3-bc4b-a4f90328c317" Tp="0" ID="53b66fb3-a0b2-49e7-828c-c803f43f401d" Ch="114"/><Tk V="1" Ft="e10c48c1-8978-49d3-bc4b-a4f90328c317" Tp="0" ID="49913557-270b-4e53-b02f-c99ecdb71305" Ch="100"/></Tokens><Formats><Format Leading="1" Size="160" ID="e10c48c1-8978-49d3-bc4b-a4f90328c317" Tracking="1" Version="2" StrokeWidth="0"><Family>Amatic SC</Family><Style>AmaticSC-Bold</Style><PostscriptName></PostscriptName><FillColor A="1" R="0" G="0.380392" B="0.521569"/><StrokeColor A="1" R="1" G="0" B="0"/></Format></Formats></TextBox><Effects/><GeometryEffects/><Masks/><LayerBase Version="2"><ID>1c591678-d523-460c-b830-72dc44b664c0</ID><Name>Title</Name><CompID>4fe99388-e1b0-415d-897f-87ba41e0ccb0</CompID><ParentLayerID>00000000-0000-0000-0000-000000000000</ParentLayerID><StartFrame>3</StartFrame><EndFrame>125</EndFrame><BlendMode>0</BlendMode><Visible>1</Visible><Muted>0</Muted><Locked>0</Locked><MotionBlurOn>0</MotionBlurOn><Label>-1</Label><BehaviorEffects><Instance Version="6"><ID>23afd1e2-0d57-44fd-8204-387ed05f73a5</ID><Name>Right Dir Insert</Name><PluginID>6489b59b-a797-4656-b0fa-55dbaee601a6</PluginID><PluginName>Right Dir Insert</PluginName><PluginVersion Re="0" Bu="0" Ma="1" Mi="0"/><ParentID>1c591678-d523-460c-b830-72dc44b664c0</ParentID><ParentTimelineID>4fe99388-e1b0-415d-897f-87ba41e0ccb0</ParentTimelineID><Enabled>1</Enabled><CreatedInComp>1</CreatedInComp><InitializedUIState>1</InitializedUIState><ParentLayerLastSize X="1920" Y="1080"/><PropertyManager Version="7"><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Error</Name><Default V="4"><st></st></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Warning</Name><Default V="4"><st></st></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Info</Name><Default V="4"><st></st></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>concealLength</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>revealLength</Name><Default V="4"><fl>25</fl></Default><Static V="4"><fl>5</fl></Static></Prop></PropertyManager><UIState><Property name="concealLength" vis="1"/><Property name="revealLength" vis="1"/></UIState></Instance></BehaviorEffects><PropertyManager Version="7"><Prop Type="0" CanInterpT="1" Spatial="1"><Name>anchorPoint</Name><Default V="4"><p3 X="0" Z="0" Y="0"/></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="1"><Name>position</Name><Default V="4"><p3 X="0" Z="0" Y="0"/></Default><Static V="4"><p3 X="-876.272" Z="0" Y="-417.792"/></Static></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>rotationY</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoSampleRadius</Name><Default V="4"><i>15</i></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>scale</Name><Default V="4"><sc X="100" Z="100" Y="100"/></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>illuminated</Name><Default V="4"><b>1</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="1"><Name>orientation</Name><Default V="4"><or X="0" Z="0" Y="0"/></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>environmentMapType</Name><Default V="4"><i>1000</i></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>scaleLinked</Name><Default V="4"><b>1</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>rotationX</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>rotationZ</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>opacity</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>receiveShadows</Name><Default V="4"><b>1</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>shadowColor</Name><Default V="4"><cl A="1" R="0" G="0" B="0"/></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>billboardedLights</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>environmentMapLayerID</Name><Default V="4"><id>00000000-0000-0000-0000-000000000000</id></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castShadows</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castAmbientOcclusion</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castShadowsIfLayerDisabled</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>billboardedShadows</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matAmbient</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>receiveAmbientOcclusion</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matDiffuse</Name><Default V="4"><fl>50</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matSpecular</Name><Default V="4"><fl>50</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoDepthFallOff</Name><Default V="4"><fl>10</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matShininess</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matEmissiveColor</Name><Default V="4"><cl A="1" R="0" G="0" B="0"/></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castReflections</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castReflectionsIfLayerDisabled</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoDepthScale</Name><Default V="4"><fl>10</fl></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>receiveReflections</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>specularReflectivity</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>diffuseReflectivity</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoSamples</Name><Default V="4"><i>4</i></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoIntensity</Name><Default V="4"><fl>50</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoBias</Name><Default V="4"><fl>0.01</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoBlurRadius</Name><Default V="4"><i>5</i></Default></Prop></PropertyManager></LayerBase></TextLayer><TextLayer Version="12"><Dimensions>0</Dimensions><IncludeInDepthMap>1</IncludeInDepthMap><TextBox Version="0"><ID>d475d9c2-f446-426b-b214-5525c1aa649f</ID><MinX>0</MinX><MaxX>373.719</MaxX><MinY>0</MinY><MaxY>111.772</MaxY><Mode>0</Mode><VerticalAlignment>2</VerticalAlignment><TopIndentation>0</TopIndentation><BottomIndentation>0</BottomIndentation><Tokens><Tk Jf="0" V="1" Tp="1" Sa="0" Sb="0" Li="0" ID="11c52651-f71f-4142-be57-b923cbd35775" Fi="0" Ri="0"/><Tk V="1" Ft="fba8de1a-8010-4d00-b30d-0a975d0793ad" Tp="0" ID="1fa0ce19-c901-43dc-853d-542e21ae47d9" Ch="68"/><Tk V="1" Ft="fba8de1a-8010-4d00-b30d-0a975d0793ad" Tp="0" ID="13d65cc5-28d8-4767-80cd-b823beb32695" Ch="111"/><Tk V="1" Ft="fba8de1a-8010-4d00-b30d-0a975d0793ad" Tp="0" ID="24f0aa1b-e7c4-4347-beb7-a6acb8087cfc" Ch="111"/><Tk V="1" Ft="fba8de1a-8010-4d00-b30d-0a975d0793ad" Tp="0" ID="c74606fd-a8d1-4d9e-9acb-3e522ff1cef7" Ch="100"/><Tk V="1" Ft="fba8de1a-8010-4d00-b30d-0a975d0793ad" Tp="0" ID="ae08e174-0832-4af6-baa1-ca9afa41674d" Ch="108"/><Tk V="1" Ft="fba8de1a-8010-4d00-b30d-0a975d0793ad" Tp="0" ID="f40a0d06-6cb2-4982-bc12-866c9958f858" Ch="101"/><Tk V="1" Ft="fba8de1a-8010-4d00-b30d-0a975d0793ad" Tp="0" ID="8028e391-22b7-408f-a1bd-f1978cea62cf" Ch="32"/><Tk V="1" Ft="fba8de1a-8010-4d00-b30d-0a975d0793ad" Tp="0" ID="99bba91f-d1e0-4444-b11d-c4919ddda4c3" Ch="80"/><Tk V="1" Ft="fba8de1a-8010-4d00-b30d-0a975d0793ad" Tp="0" ID="01d2491b-1a08-49f2-ba8a-0117778a96fe" Ch="97"/><Tk V="1" Ft="fba8de1a-8010-4d00-b30d-0a975d0793ad" Tp="0" ID="6cfafe72-3e32-4b45-9f03-10f8b703fb79" Ch="99"/><Tk V="1" Ft="fba8de1a-8010-4d00-b30d-0a975d0793ad" Tp="0" ID="d5b6322d-0934-4462-8d28-19e25fa92449" Ch="107"/></Tokens><Formats><Format Leading="1" Size="110" ID="fba8de1a-8010-4d00-b30d-0a975d0793ad" Tracking="1" Version="2" StrokeWidth="0"><Family>Amatic SC</Family><Style>AmaticSC-Bold</Style><PostscriptName></PostscriptName><FillColor A="1" R="0" G="0.380392" B="0.521569"/><StrokeColor A="1" R="1" G="0" B="0"/></Format></Formats></TextBox><Effects/><GeometryEffects/><Masks/><LayerBase Version="2"><ID>8b91dad2-1f68-4ab4-8f54-f397f4029c9d</ID><Name>Subtitle</Name><CompID>4fe99388-e1b0-415d-897f-87ba41e0ccb0</CompID><ParentLayerID>00000000-0000-0000-0000-000000000000</ParentLayerID><StartFrame>5</StartFrame><EndFrame>125</EndFrame><BlendMode>0</BlendMode><Visible>1</Visible><Muted>0</Muted><Locked>0</Locked><MotionBlurOn>0</MotionBlurOn><Label>-1</Label><BehaviorEffects><Instance Version="6"><ID>750bc2d2-c8f5-4b03-8cf2-049c70e8fbe9</ID><Name>Right Dir Insert</Name><PluginID>6489b59b-a797-4656-b0fa-55dbaee601a6</PluginID><PluginName>Right Dir Insert</PluginName><PluginVersion Re="0" Bu="0" Ma="1" Mi="0"/><ParentID>8b91dad2-1f68-4ab4-8f54-f397f4029c9d</ParentID><ParentTimelineID>4fe99388-e1b0-415d-897f-87ba41e0ccb0</ParentTimelineID><Enabled>1</Enabled><CreatedInComp>1</CreatedInComp><InitializedUIState>1</InitializedUIState><ParentLayerLastSize X="1920" Y="1080"/><PropertyManager Version="7"><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Error</Name><Default V="4"><st></st></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Warning</Name><Default V="4"><st></st></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Info</Name><Default V="4"><st></st></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>concealLength</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>revealLength</Name><Default V="4"><fl>25</fl></Default><Static V="4"><fl>5</fl></Static></Prop></PropertyManager><UIState><Property name="concealLength" vis="1"/><Property name="revealLength" vis="1"/></UIState></Instance></BehaviorEffects><PropertyManager Version="7"><Prop Type="0" CanInterpT="1" Spatial="1"><Name>position</Name><Default V="4"><p3 X="0" Z="0" Y="0"/></Default><Static V="4"><p3 X="-332.41" Z="0" Y="-410.273"/></Static></Prop><Prop Type="0" CanInterpT="1" Spatial="1"><Name>anchorPoint</Name><Default V="4"><p3 X="0" Z="0" Y="0"/></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>rotationY</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>scale</Name><Default V="4"><sc X="100" Z="100" Y="100"/></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoSampleRadius</Name><Default V="4"><i>15</i></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="1"><Name>orientation</Name><Default V="4"><or X="0" Z="0" Y="0"/></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>illuminated</Name><Default V="4"><b>1</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>scaleLinked</Name><Default V="4"><b>1</b></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>environmentMapType</Name><Default V="4"><i>1000</i></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>rotationX</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>rotationZ</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>opacity</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>receiveShadows</Name><Default V="4"><b>1</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>environmentMapLayerID</Name><Default V="4"><id>00000000-0000-0000-0000-000000000000</id></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>billboardedLights</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>shadowColor</Name><Default V="4"><cl A="1" R="0" G="0" B="0"/></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castAmbientOcclusion</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castShadows</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castShadowsIfLayerDisabled</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>billboardedShadows</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>receiveAmbientOcclusion</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matAmbient</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matDiffuse</Name><Default V="4"><fl>50</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoDepthFallOff</Name><Default V="4"><fl>10</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matSpecular</Name><Default V="4"><fl>50</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matShininess</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matEmissiveColor</Name><Default V="4"><cl A="1" R="0" G="0" B="0"/></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castReflections</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoDepthScale</Name><Default V="4"><fl>10</fl></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castReflectionsIfLayerDisabled</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>receiveReflections</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>specularReflectivity</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>diffuseReflectivity</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoSamples</Name><Default V="4"><i>4</i></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoIntensity</Name><Default V="4"><fl>50</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoBias</Name><Default V="4"><fl>0.01</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoBlurRadius</Name><Default V="4"><i>5</i></Default></Prop></PropertyManager></LayerBase></TextLayer><AssetLayer Version="15"><AssetID>f69f51ab-2a8c-46ae-9e91-f4f29b736b86</AssetID><AssetInstanceStart>0</AssetInstanceStart><AssetHasAudio>1</AssetHasAudio><AssetHasVideo>1</AssetHasVideo><AssetHadAudio>1</AssetHadAudio><AssetHadVideo>1</AssetHadVideo><AssetType>0</AssetType><Dimensions>0</Dimensions><AutoOrient>0</AutoOrient><AutoOrientPathAxis>1</AutoOrientPathAxis><AutoOrientLayer>00000000-0000-0000-0000-000000000000</AutoOrientLayer><PromoteLights>0</PromoteLights><IncludeInDepthMap>1</IncludeInDepthMap><WaveformIsVisible>0</WaveformIsVisible><Trackers/><Effects><Instance Version="6"><ID>7576bc96-14fe-4b4f-bf56-dc44e1618d98</ID><Name>Set Matte</Name><PluginID>10ded6c2-ff84-40fe-8bd9-4127bfb44f16</PluginID><PluginName>Set Matte</PluginName><PluginVersion Re="0" Bu="0" Ma="1" Mi="2"/><ParentID>965d2514-208d-4d80-a0fb-2e1f7ba60074</ParentID><ParentTimelineID>4fe99388-e1b0-415d-897f-87ba41e0ccb0</ParentTimelineID><Enabled>1</Enabled><CreatedInComp>1</CreatedInComp><InitializedUIState>1</InitializedUIState><ParentLayerLastSize X="1440" Y="360"/><PropertyManager Version="7"><Prop Type="0" CanInterpT="0" Spatial="0"><Name>invert</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="0" CanInterpT="0" Spatial="0"><Name>matteBlend</Name><Default V="4"><i>2</i></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>pluginPreset</Name><Default V="4"><i>0</i></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Error</Name><Default V="4"><st></st></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>sourceLayer:IgnoreInvisible</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Warning</Name><Default V="4"><st></st></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Info</Name><Default V="4"><st></st></Default></Prop><Prop Type="0" CanInterpT="0" Spatial="0"><Name>matteChannel</Name><Default V="4"><i>3</i></Default><Static V="4"><i>1</i></Static></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>sourceLayer</Name><Default V="4"><id>00000000-0000-0000-0000-000000000000</id></Default><Static V="4"><id>bbf5795c-d0d2-4dcd-b829-1b3e8ae13ce5</id></Static></Prop></PropertyManager><UIState><Property name="invert" vis="1"/><Property name="matteBlend" vis="1"/><Property name="sourceLayer:IgnoreInvisible" vis="0"/><Property name="matteChannel" vis="1"/><Property name="sourceLayer" vis="1"/></UIState></Instance></Effects><Masks/><LayerBase Version="2"><ID>965d2514-208d-4d80-a0fb-2e1f7ba60074</ID><Name>Doodle Pack - Lowerthird 1.mp4</Name><CompID>4fe99388-e1b0-415d-897f-87ba41e0ccb0</CompID><ParentLayerID>00000000-0000-0000-0000-000000000000</ParentLayerID><StartFrame>0</StartFrame><EndFrame>125</EndFrame><BlendMode>0</BlendMode><Visible>1</Visible><Muted>0</Muted><Locked>0</Locked><MotionBlurOn>0</MotionBlurOn><Label>-1</Label><BehaviorEffects/><PropertyManager Version="7"><Prop Type="0" CanInterpT="1" Spatial="0"><Name>rotationY</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="1"><Name>anchorPoint</Name><Default V="4"><p3 X="0" Z="0" Y="0"/></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="1"><Name>position</Name><Default V="4"><p3 X="0" Z="0" Y="0"/></Default><Static V="4"><p3 X="-240" Z="0" Y="-360"/></Static></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>illuminated</Name><Default V="4"><b>1</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="1"><Name>orientation</Name><Default V="4"><or X="0" Z="0" Y="0"/></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoSampleRadius</Name><Default V="4"><i>15</i></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>scale</Name><Default V="4"><sc X="100" Z="100" Y="100"/></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>scaleLinked</Name><Default V="4"><b>1</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>rotationX</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>rotationZ</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>opacity</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castShadowsIfLayerDisabled</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>audioLevel</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>receiveReflections</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>speed</Name><Default V="4"><db>1</db></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>receiveShadows</Name><Default V="4"><b>1</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>billboardedLights</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>shadowColor</Name><Default V="4"><cl A="1" R="0" G="0" B="0"/></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castAmbientOcclusion</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castShadows</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>billboardedShadows</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>receiveAmbientOcclusion</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matAmbient</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matDiffuse</Name><Default V="4"><fl>50</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoDepthFallOff</Name><Default V="4"><fl>10</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matSpecular</Name><Default V="4"><fl>50</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matShininess</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matEmissiveColor</Name><Default V="4"><cl A="1" R="0" G="0" B="0"/></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castReflections</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoDepthScale</Name><Default V="4"><fl>10</fl></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castReflectionsIfLayerDisabled</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>specularReflectivity</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoSamples</Name><Default V="4"><i>4</i></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoIntensity</Name><Default V="4"><fl>50</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoBias</Name><Default V="4"><fl>0.01</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoBlurRadius</Name><Default V="4"><i>5</i></Default></Prop></PropertyManager></LayerBase></AssetLayer><AssetLayer Version="15"><AssetID>a9a3772c-ce0a-43aa-8047-f93545b08132</AssetID><AssetInstanceStart>0</AssetInstanceStart><AssetHasAudio>1</AssetHasAudio><AssetHasVideo>1</AssetHasVideo><AssetHadAudio>1</AssetHadAudio><AssetHadVideo>1</AssetHadVideo><AssetType>0</AssetType><Dimensions>0</Dimensions><AutoOrient>0</AutoOrient><AutoOrientPathAxis>1</AutoOrientPathAxis><AutoOrientLayer>00000000-0000-0000-0000-000000000000</AutoOrientLayer><PromoteLights>0</PromoteLights><IncludeInDepthMap>1</IncludeInDepthMap><WaveformIsVisible>0</WaveformIsVisible><Trackers/><Effects><Instance Version="6"><ID>96871dc7-e8a3-4c2d-a1a1-759202ea8c88</ID><Name>Color Space Converter</Name><PluginID>3cf99270-695a-47d8-877c-c37963e017c9</PluginID><PluginName>Color Space Converter</PluginName><PluginVersion Re="0" Bu="0" Ma="1" Mi="2"/><ParentID>bbf5795c-d0d2-4dcd-b829-1b3e8ae13ce5</ParentID><ParentTimelineID>4fe99388-e1b0-415d-897f-87ba41e0ccb0</ParentTimelineID><Enabled>0</Enabled><CreatedInComp>1</CreatedInComp><InitializedUIState>1</InitializedUIState><ParentLayerLastSize X="1440" Y="360"/><PropertyManager Version="7"><Prop Type="1" CanInterpT="1" Spatial="0"><Name>pluginPreset</Name><Default V="4"><i>0</i></Default></Prop><Prop Type="0" CanInterpT="0" Spatial="0"><Name>fromCombo</Name><Default V="4"><i>0</i></Default><Static V="4"><i>4</i></Static></Prop><Prop Type="0" CanInterpT="0" Spatial="0"><Name>invert</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Error</Name><Default V="4"><st></st></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Warning</Name><Default V="4"><st></st></Default></Prop><Prop Type="0" CanInterpT="0" Spatial="0"><Name>toCombo</Name><Default V="4"><i>0</i></Default><Static V="4"><i>6</i></Static></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Info</Name><Default V="4"><st></st></Default></Prop><Prop Type="0" CanInterpT="0" Spatial="0"><Name>alphaType</Name><Default V="4"><i>0</i></Default></Prop></PropertyManager><UIState><Property name="invert" vis="1"/><Property name="fromCombo" vis="1"/><Property name="toCombo" vis="1"/><Property name="alphaType" vis="1"/></UIState></Instance><Instance Version="6"><ID>7449673f-9a9f-4fb0-b746-456ec2a9d53d</ID><Name>Fill Color</Name><PluginID>08cf3da2-59fb-4a57-acb2-31f34cefd493</PluginID><PluginName>Fill Color</PluginName><PluginVersion Re="0" Bu="0" Ma="1" Mi="2"/><ParentID>bbf5795c-d0d2-4dcd-b829-1b3e8ae13ce5</ParentID><ParentTimelineID>4fe99388-e1b0-415d-897f-87ba41e0ccb0</ParentTimelineID><Enabled>0</Enabled><CreatedInComp>1</CreatedInComp><InitializedUIState>1</InitializedUIState><ParentLayerLastSize X="1440" Y="360"/><PropertyManager Version="7"><Prop Type="1" CanInterpT="1" Spatial="0"><Name>pluginPreset</Name><Default V="4"><i>0</i></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Error</Name><Default V="4"><st></st></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Warning</Name><Default V="4"><st></st></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>HF_Persistant_Message_Info</Name><Default V="4"><st></st></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>fillColor</Name><Default V="4"><cl A="1" R="1" G="1" B="1"/></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>blendAmount</Name><Default V="4"><fl>75</fl></Default><Static V="4"><fl>100</fl></Static></Prop></PropertyManager><UIState><Property name="fillColor" vis="1"/><Property name="blendAmount" vis="1"/></UIState></Instance></Effects><Masks/><LayerBase Version="2"><ID>bbf5795c-d0d2-4dcd-b829-1b3e8ae13ce5</ID><Name>Doodle Pack - Lowerthird 1_L0.mp4</Name><CompID>4fe99388-e1b0-415d-897f-87ba41e0ccb0</CompID><ParentLayerID>00000000-0000-0000-0000-000000000000</ParentLayerID><StartFrame>0</StartFrame><EndFrame>125</EndFrame><BlendMode>0</BlendMode><Visible>0</Visible><Muted>0</Muted><Locked>0</Locked><MotionBlurOn>0</MotionBlurOn><Label>-1</Label><BehaviorEffects/><PropertyManager Version="7"><Prop Type="0" CanInterpT="1" Spatial="1"><Name>anchorPoint</Name><Default V="4"><p3 X="0" Z="0" Y="0"/></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="1"><Name>position</Name><Default V="4"><p3 X="0" Z="0" Y="0"/></Default><Static V="4"><p3 X="-240" Z="0" Y="-360"/></Static></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>rotationY</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoSampleRadius</Name><Default V="4"><i>15</i></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>scale</Name><Default V="4"><sc X="100" Z="100" Y="100"/></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>illuminated</Name><Default V="4"><b>1</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="1"><Name>orientation</Name><Default V="4"><or X="0" Z="0" Y="0"/></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>scaleLinked</Name><Default V="4"><b>1</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>rotationX</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>rotationZ</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>opacity</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>audioLevel</Name><Default V="4"><fl>0</fl></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castShadowsIfLayerDisabled</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>speed</Name><Default V="4"><db>1</db></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>receiveReflections</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>receiveShadows</Name><Default V="4"><b>1</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>shadowColor</Name><Default V="4"><cl A="1" R="0" G="0" B="0"/></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>billboardedLights</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castShadows</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castAmbientOcclusion</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>billboardedShadows</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matAmbient</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>receiveAmbientOcclusion</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matDiffuse</Name><Default V="4"><fl>50</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matSpecular</Name><Default V="4"><fl>50</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoDepthFallOff</Name><Default V="4"><fl>10</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matShininess</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>matEmissiveColor</Name><Default V="4"><cl A="1" R="0" G="0" B="0"/></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castReflections</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="0" Spatial="0"><Name>castReflectionsIfLayerDisabled</Name><Default V="4"><b>0</b></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoDepthScale</Name><Default V="4"><fl>10</fl></Default></Prop><Prop Type="0" CanInterpT="1" Spatial="0"><Name>specularReflectivity</Name><Default V="4"><fl>100</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoSamples</Name><Default V="4"><i>4</i></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoIntensity</Name><Default V="4"><fl>50</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoBias</Name><Default V="4"><fl>0.01</fl></Default></Prop><Prop Type="1" CanInterpT="1" Spatial="0"><Name>aoBlurRadius</Name><Default V="4"><i>5</i></Default></Prop></PropertyManager></LayerBase></AssetLayer></Layers><Instances/><ViewerState Version="4"><CurrentLayout>0</CurrentLayout><Layout0 Pos0="3e8e68f3-8722-4a90-af37-272784aa9d67"/><Layout1/><Layout2 Sp1="0" Sp2="0" Sp0="0.5"/><Layout3 Sp1="0" Sp2="0.5" Sp0="0.5"/><Layout4 Sp1="0.5" Sp2="0.5" Sp0="0.5"/><Views><State TextureScale="0.448624" CameraScale="1" Layout="0" Type="0" ID="3e8e68f3-8722-4a90-af37-272784aa9d67" Active="1"><TexturePosition X="0" Y="0"/><TextureAnchorPoint X="0" Y="0"/><CameraPosition X="0" Z="0" Y="0"/><CameraRotation X="0" Z="0" Y="0"/><Options Vol="1" WoAx="1" Gz="0" TrCb="1" BiTo="1" TrPa="1" MoPa="1" Ch="0"><BGColor A="0" R="0" G="0" B="0"/></Options></State></Views></ViewerState><CompositionTemplate Version="0"><TreeNode Version="0"><Type>0</Type><BaseNode Version="0"><DisplayName></DisplayName><PropertyName></PropertyName><Options>0</Options><ChildNodes><ButtonNode Version="0"><BaseNode Version="0"><DisplayName>Edit Title</DisplayName><PropertyName>cb8faf8b-b305-422c-ae3d-83985de27acf</PropertyName><Options>0</Options><ChildNodes/></BaseNode></ButtonNode><ButtonNode Version="0"><BaseNode Version="0"><DisplayName>Edit Subtitle</DisplayName><PropertyName>f92ff94a-5c93-4786-89c7-ffec825beb70</PropertyName><Options>0</Options><ChildNodes/></BaseNode></ButtonNode></ChildNodes></BaseNode></TreeNode><TemplateProperty><Name>cb8faf8b-b305-422c-ae3d-83985de27acf</Name><CompositionProperty Version="0"><Type>0</Type><LayerAttribute>1</LayerAttribute><LayerID>1c591678-d523-460c-b830-72dc44b664c0</LayerID><SubObjectID>00000000-0000-0000-0000-000000000000</SubObjectID><Name></Name></CompositionProperty></TemplateProperty><TemplateProperty><Name>f92ff94a-5c93-4786-89c7-ffec825beb70</Name><CompositionProperty Version="0"><Type>0</Type><LayerAttribute>1</LayerAttribute><LayerID>8b91dad2-1f68-4ab4-8f54-f397f4029c9d</LayerID><SubObjectID>00000000-0000-0000-0000-000000000000</SubObjectID><Name></Name></CompositionProperty></TemplateProperty></CompositionTemplate><TemplateParent>00000000-0000-0000-0000-000000000000</TemplateParent></CompositionAsset></BiffCompositeShot>
'''


def debug_log(file, string):
    f = open(file, 'a')
    f.write(str(string) + "\n")
    f.close()


def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        # print(path + ' -- Folder Created Successfully')
        os.makedirs(path)
        return True
    else:
        # print(path + ' -- Folder Already Exists')
        return False


def xml2dict(xmlstr):
    xmlparse = xmltodict.parse(xmlstr)
    jsonData = json.dumps(xmlparse)
    dictData = json.loads(jsonData)
    return dictData


def dict2xml(dict):
    xml = xmltodict.unparse(dict, pretty=True)
    regex = re.compile(r"></(.*?)>", re.IGNORECASE)
    final = regex.sub('/>', xml)
    return final


def code2text(code):
    hexmap = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "A": 10, "B": 11, "C": 12,
              "D": 13, "E": 14, "F": 15, }
    texts = []
    for i in range(int(len(code) / 4)):
        k = code[4 * i:4 * (i + 1)]
        x = hexmap[k[3]] + hexmap[k[2]] * 16 + hexmap[k[1]] * 16 * 16 + hexmap[k[0]] * 16 * 16 * 16
        texts.append(x)
    return texts


def intARGB2ARGB(val):
    color = str(hex((val + (1 << 32)) % (1 << 32))).replace("0x", "")
    A = int(color[0] + color[1], 16)
    R = int(color[2] + color[3], 16)
    G = int(color[4] + color[5], 16)
    B = int(color[6] + color[7], 16)

    return A, B, G, R


def intARGB2intRGB(val):
    color = str(hex((val + (1 << 32)) % (1 << 32))).replace("0x", "")
    if len(color) == 8:
        hexColor = color[6] + color[7] + color[4] + color[5] + color[2] + color[3]
    if len(color) == 6:
        hexColor = color[4] + color[5] + color[2] + color[3] + color[0] + color[1]
    return int(hexColor, 16)


def int2RGB(val):
    print('Color Index:',val)
    if val == 0:
        return 0.0,0.0,0.0

    color = str(hex(val)).replace('0x', '')
    R = int(color[0:2], 16)
    G = int(color[2:4], 16)
    B = int(color[4:6], 16)

    f_R = R / 255
    f_G = G / 255
    f_B = B / 255

    return f_R, f_G, f_B


def textcode2token(textcodeList, GUID):
    token = []
    header = {'@V': '1', '@Tp': '1', '@Jf': '1', '@Li': '0', '@Ri': '0', '@Fi': '0', '@Sb': '0', '@Sa': '0'}
    token.append(header)
    for textcode in textcodeList:
        Tk = {'@V': '1', '@Tp': '0', '@Ch': str(textcode), '@Ft': GUID}
        token.append(Tk)
    return token


def create_main(XMLstr):
    rawGUID = set(re.findall('........-....-....-....-............', XMLstr))

    fixGUID = ['00000000-0000-0000-0000-000000000000',
               '10ded6c2-ff84-40fe-8bd9-4127bfb44f16',
               '01201F5E-4BE5-4388-ADF1-16B0A924C1F8'
               ]
    for GUID in rawGUID:
        if GUID in fixGUID:
            pass
        else:
            newGUID = str(uuid.uuid4()).upper()
            XMLstr = XMLstr.replace(GUID, newGUID)
    title = xml2dict(XMLstr)

    return title


def create_key():
    key = {}

    comp = {
        'name': 'Doodle Pack - Lowerthird 1',

        'OutPoint': 125,
        'FrameCount': 125,
        'Width': 1920,
        'Height': 1080,
        'FrameRate': 25.0
    }

    media = {

        'media0': 'Doodle Pack - Lowerthird 1.mp4',
        'media1': 'Doodle Pack - Lowerthird 1_L0.mp4'

    }

    text = {
        'Text': 'Hello World',

        'Family': 'Amatic SC',
        'Style': 'Amatic SC Bold',
        'PostscriptName': 'AmaticSC-Bold',
        'FillColor': {'R': 0.0, 'G': 0.380392, 'B': 0.521569, 'A': 1.0},
        'StrokeColor': {'R': 1.0, 'G': 0.0, 'B': 0.0, 'A': 1.0},
        'Size': 160,
        'StrokeWidth': 0,
        'Tracking': 1,
        'Leading': 1,

        'anchorPoint': {'X': 0.0, 'Y': 0.0},
        'position': {'X': -876.272, 'Y': -417.792},
        'scale': 1.0,
        'rotationZ': 0.0,
        'opacity': 100.0,

        'StartFrame': 0,
        'EndFrame': 125,
        'MinX': 0,
        'MaxX': 491.641,
        'MinY': 0,
        'MaxY': 162.578,
        'BlendMode': 0,
        'Visible': 1,
        'MotionBlur': 0,
        'Mode': 0,
        'VerticalAlignment': 2,
        'TopIndentation': 0,
        'BottomIndentation': 0,

        'Animation': 20,
        'RevealLength': 5,
        'ConcealLength': 0,
    }

    key['comp'] = comp
    key['media'] = media
    key['text'] = text

    Title = {}
    Title['Title'] = key
    print(dict2xml(Title))


def get_key(path):
    # get all the useful key value from Filmora Effect data.xml

    print('Getting Data from:', path)
    file = open(path, 'r').read()
    data = xml2dict(file)

    key = {}

    name = path.split('/')[-3]
    Framerate = float(get_value(data['TimeLine']['Properties']['Property'], 'Render.Framerate').split(': ')[1])
    TotalFrameCount = int(get_value(data['TimeLine']['Properties']['Property'], 'Render.TotalFrameCount'))

    key['name'] = name
    key['Framerate'] = Framerate
    key['TotalFrameCount'] = TotalFrameCount

    if 'Absolute.FilePath' in file:
        try:
            media0 = re.search(r'kAlphaVideo_FullHDDataFilepath(.*?)\"/>', file).group(1).split('/')[1]
            media1 = re.search(r'Absolute\.FilePath(.*?)\"/>', file).group(1).split('/')[1]
            key['WithMedia'] = True
            key['media0'] = media0
            key['media1'] = media1
        except:
            pass
    else:
        key['WithMedia'] = False

    key['texts'] = []

    if type(data['TimeLine']['TimeLine']) is list:
        for timeline in data['TimeLine']['TimeLine']:
            if 'kAlphaVideo_FullHDDataFilepath' in str(timeline):

                key['media_Angel'] = float(get_value(timeline['Properties']['Property'], 'Transform.Angle'))
                key['media_POS_X'] = (float(get_value(timeline['Properties']['Property'], 'Transform.CenterPoint').split(',')[0].split(':')[1]) - 0.5) * 1920
                key['media_POS_Y'] = (float(get_value(timeline['Properties']['Property'], 'Transform.CenterPoint').split(',')[1].split(':')[1]) - 0.5) * (-1080)
                key['media_Scale'] = float(get_value(timeline['Properties']['Property'], 'Transform.ResizeScale').split(',')[0].split(':')[1]) * 100


            elif get_textinfo(timeline) is None:
                pass
            else:
                key['texts'].append(get_textinfo(timeline))
    elif type(data['TimeLine']['TimeLine']) is dict:
        if get_textinfo(data['TimeLine']['TimeLine']) is None:
            pass
        else:
            key['texts'].append(get_textinfo(data['TimeLine']['TimeLine']))

    print('Get Key from:', path, '\n', key)
    print("With Media Layer:", key['WithMedia'])
    print("Count of Texts:", len(key['texts']))
    print('\n')

    return key


def get_textinfo(timeline):
    if 'Text.Section.CaptionData' in str(timeline):
        text_xml = get_value(timeline['Properties']['Property'], 'Text.Section.CaptionData')
        text_dict = xml2dict(text_xml)

        text_node = text_dict['NLETitleArray']['NLETitleItem']['TextNode']

        text = text_node['TextParam']['TextData']['CharData']['@Title']
        FontName = text_node['TextParam']['TextData']['CharData']['Font']['@FontName']
        FontSize = text_node['TextParam']['TextData']['CharData']['Font']['@Size']
        FontFillColor = text_node['TextParam']['TextData']['CharData']['Face']['@Color1']
        RowSpace = text_node['TextParam']['TextData']['CharData']['@RowSpace']

        FontAngle = get_value(timeline['Properties']['Property'], "Transform.Angle")
        FontCenterPoint_X = float(
            get_value(timeline['Properties']['Property'], "Transform.CenterPoint").split(',')[0].split(':')[1])
        FontCenterPoint_Y = float(
            get_value(timeline['Properties']['Property'], "Transform.CenterPoint").split(',')[1].split(':')[1])

        FontScale = float(
            get_value(timeline['Properties']['Property'], "Transform.ResizeScale").split(',')[1].split(':')[1])

        FontStartFrame = int(get_value(timeline['Properties']['Property'], "Render.Position"))
        FontEndFrame = int(
            get_value(timeline['Properties']['Property'], "Render.RangeFrameNumber").split(',')[1].split(':')[
                1]) + FontStartFrame

        FontLeftRange = int(get_value(timeline['Properties']['Property'], "xfer.left.range.Video"))
        FontRightRange = int(get_value(timeline['Properties']['Property'], "xfer.right.range.Video"))

        text_info = {}
        text_info['text'] = code2text(text)
        text_info['FontName'] = FontName
        text_info['FontSize'] = FontSize
        text_info['RowSpace'] = RowSpace
        text_info['FontFillColor'] = FontFillColor
        text_info['FontAngle'] = FontAngle
        text_info['FontCenterPoint_X'] = FontCenterPoint_X
        text_info['FontCenterPoint_Y'] = FontCenterPoint_Y
        text_info['FontScale'] = FontScale
        text_info['FontStartFrame'] = FontStartFrame
        text_info['FontEndFrame'] = FontEndFrame
        text_info['FontLeftRange'] = FontLeftRange
        text_info['FontRightRange'] = FontRightRange
        return text_info


def get_value(list, key):
    if key in str(list):
        for item in list:
            if item['@key'] == key:
                return item['@value']
            else:
                pass
    else:
        return 0


def getFontInfo(name):
    path = 'Example/Fonts.json'
    file = open(path, 'r').read()
    fonts = json.loads(file)['Fonts']

    if name not in file:
        name = "Open Sans"

    for font in fonts:
        if name == font['Style']:
            return font['family'], font['Style'], font['PostscriptName']

    for font in fonts:
        if name in font['Style']:
            return font['family'], font['Style'], font['PostscriptName']

    for font in fonts:
        if name in font['PostscriptName']:
            return font['family'], font['Style'], font['PostscriptName']

    for font in fonts:
        if name in font['textfile']:
            return font['family'], font['Style'], font['PostscriptName']

def getAllFiles(path):
    tempfiles = []
    for i in os.listdir(path):
        tempPath = os.path.join(path, i)
        if os.path.isfile(tempPath):
            tempfiles.append(tempPath)
            # print("Append Path:",tempPath)
        else:
            tempfiles += getAllFiles(tempPath)
    return tempfiles


def setupNewFolder(old, new):
    oldFontFolder = os.path.join(old, 'Font')
    oldDataFolder = os.path.join(old, 'Data')
    # print(old,'\n',new)
    newMediaFolder = os.path.join(new, 'Media')
    newFontFolder = os.path.join(new, 'Fonts')
    mkdir(newMediaFolder)
    mkdir(newFontFolder)
    for i in os.listdir(oldFontFolder):
        fontFile = os.path.join(oldFontFolder, i)
        shutil.copy(fontFile, newFontFolder)
    for i in os.listdir(oldDataFolder):
        if ".mp4" in i:
            meidaFile = os.path.join(oldDataFolder, i)
            shutil.copy(meidaFile, newMediaFolder)
    for i in os.listdir(old):
        if '.bmp' in i or '.jpg' in i or '.png' in i:
            thumbnail = os.path.join(old, i)
            img = Image.open(thumbnail)
            name = new.split('/')[-1].replace('.wfptitle', '') + '.png'
            tgaThumbnail = os.path.join(new, name)
            img.save(tgaThumbnail, 'png')
    print('Finish Seting Up The Folder :', new)


def create_VBG_TSF(key):
    r = key['media_Angel']
    x = key['media_POS_X']
    y = key['media_POS_Y']
    s = key['media_Scale']
    s = 100

    VBG_TSF = {'@Version': '7',
               'Prop': [
                   {'@CanInterpT': '1', '@Spatial': '1', '@Type': '0', 'Name': 'anchorPoint',
                    'Default': {'@V': '4', 'p3': {'@X': '0', '@Y': '0', '@Z': '0'}}},
                   {'@CanInterpT': '1', '@Spatial': '1', '@Type': '0', 'Name': 'position',
                    'Default': {'@V': '4', 'p3': {'@X': x, '@Y': y, '@Z': '0'}}},
                   {'@CanInterpT': '1', '@Spatial': '0', '@Type': '0', 'Name': 'scale',
                    'Default': {'@V': '4', 'sc': {'@X': s, '@Y': s, '@Z': s}}},
                   {'@CanInterpT': '0', '@Spatial': '0', '@Type': '1', 'Name': 'scaleLinked',
                    'Default': {'@V': '4', 'b': '1'}},
                   {'@CanInterpT': '1', '@Spatial': '0', '@Type': '0', 'Name': 'rotationZ',
                    'Default': {'@V': '4', 'fl': r}},
                   {'@CanInterpT': '1', '@Spatial': '0', '@Type': '0', 'Name': 'opacity',
                    'Default': {'@V': '4', 'fl': '100'}}
               ]
               }
    return VBG_TSF


def create_Text_TSF(key):
    y_offset = float(key['FontSize'])*0.86

    r = float(key['FontAngle'])
    x = (float(key['FontCenterPoint_X'])-0.5)*1920
    y = (float(key['FontCenterPoint_Y'])-0.5)*(-1080)- y_offset
    s = key['FontScale']



    Text_TSF = {'@Version': '7',
                'Prop': [{'@CanInterpT': '1', '@Spatial': '1', '@Type': '0', 'Name': 'anchorPoint',
                          'Default': {'@V': '4', 'p3': {'@X': '0', '@Y': '0', '@Z': '0'}}},
                         {'@CanInterpT': '1', '@Spatial': '1', '@Type': '0', 'Name': 'position',
                          'Default': {'@V': '4', 'p3': {'@X': x, '@Y': y, '@Z': '0'}}},
                         {'@CanInterpT': '1', '@Spatial': '0', '@Type': '0', 'Name': 'scale',
                          'Default': {'@V': '4', 'sc': {'@X': '100', '@Y': '100', '@Z': '100'}}},
                         {'@CanInterpT': '0', '@Spatial': '0', '@Type': '1', 'Name': 'scaleLinked',
                          'Default': {'@V': '4', 'b': '1'}},
                         {'@CanInterpT': '1', '@Spatial': '0', '@Type': '0', 'Name': 'rotationZ',
                          'Default': {'@V': '4', 'fl': r}},
                         {'@CanInterpT': '1', '@Spatial': '0', '@Type': '0', 'Name': 'opacity',
                          'Default': {'@V': '4', 'fl': '100'}}
                         ]}
    return Text_TSF



def create_offset(name,index,TextRefLayer):
    path = 'Example/Offset.json'

    if os.path.isfile(path):
        file = open(path, 'r').read()
        offset = json.loads(file)
        if name in offset:
            pass
        else:
            offset[name] = {}
    else:
        offset = {}
        offset[name] = {}
    offset[name][str(index)] = {}
    offset[name][str(index)]['Offset_X'] = 0
    offset[name][str(index)]['Offset_Y'] = 0
    offset[name][str(index)]['Animation'] = 10
    offset[name][str(index)]['FontSize'] = TextRefLayer['TextBox']['Formats']['Format']['@Size']
    offset[name][str(index)]['family'] = TextRefLayer['TextBox']['Formats']['Format']['Family']
    offset[name][str(index)]['Style'] = TextRefLayer['TextBox']['Formats']['Format']['Style']
    offset[name][str(index)]['PostscriptName'] = TextRefLayer['TextBox']['Formats']['Format']['PostscriptName']

    offset_str = json.dumps(offset ,sort_keys=True, indent=4, separators=(',', ':'))
    f = open(path,'w')
    f.write(offset_str)
    f.close()



def setOffset(name,index,TextRefLayer):
    path = 'Example/Offset.json'
    file = open(path,'r').read()
    offset = json.loads(file)

    if str(index) in offset[name]:
        raw_X = float(TextRefLayer['PropertyManager']['Prop'][1]['Default']['p3']['@X'])
        raw_Y = float(TextRefLayer['PropertyManager']['Prop'][1]['Default']['p3']['@Y'])
        TextRefLayer['PropertyManager']['Prop'][1]['Default']['p3']['@X'] = raw_X - offset[name][str(index)]['Offset_X']
        TextRefLayer['PropertyManager']['Prop'][1]['Default']['p3']['@Y'] = raw_Y - offset[name][str(index)]['Offset_Y']
        TextRefLayer['Effects']['Instance']['PropertyManager']['Prop'][0]['Default']['i'] = offset[name][str(index)]['Animation']
        TextRefLayer['TextBox']['Formats']['Format']['@Size'] = offset[name][str(index)]['FontSize']
        TextRefLayer['TextBox']['Formats']['Format']['Family'] = offset[name][str(index)]['family']
        TextRefLayer['TextBox']['Formats']['Format']['Style'] = offset[name][str(index)]['Style']
        TextRefLayer['TextBox']['Formats']['Format']['PostscriptName'] = offset[name][str(index)]['PostscriptName']
        print("Finish Offset:",-offset[name][str(index)]['Offset_X'],-offset[name][str(index)]['Offset_Y'])

    return TextRefLayer

def create_title(file, new):
    key = get_key(file)

    path = 'Example/example1.wfptitle'
    xmlstr = open(path, 'r').read()
    title = create_main(xmlstr)

    title['BiffCompositeShot']['CompositionAsset']['Name'] = key['name']
    title['BiffCompositeShot']['CompositionAsset']['OutPoint'] = key['TotalFrameCount']
    title['BiffCompositeShot']['CompositionAsset']['AudioVideoSettings']['FrameCount'] = key['TotalFrameCount']
    title['BiffCompositeShot']['CompositionAsset']['AudioVideoSettings']['FrameRate'] = key['Framerate']

    del title['BiffCompositeShot']['CompositionAsset']['CompositionTemplate']['TemplateProperty']
    del title['BiffCompositeShot']['CompositionAsset']['CompositionTemplate']['TreeNode']['BaseNode']['ChildNodes'][
        'ButtonNode']
    del title['BiffCompositeShot']['CompositionAsset']['CompositionTemplate']['TreeNode']['BaseNode']['ChildNodes'][
        'TreeNode']
    del title['BiffCompositeShot']['CompositionAsset']['Layers']['TextRefLayer']

    if key['WithMedia']:
        title['BiffCompositeShot']['AssetRefs']['Media'][0]['Filename'] = 'Media/' + key['media0']
        title['BiffCompositeShot']['AssetRefs']['Media'][1]['Filename'] = 'Media/' + key['media1']

        VBGs = title['BiffCompositeShot']['CompositionAsset']['Layers']['AssetRefLayer']
        for VBG in VBGs:
            VBG['EndFrame'] = key['TotalFrameCount']
            VBG['PropertyManager'] = create_VBG_TSF(key)

    else:
        del title['BiffCompositeShot']['AssetRefs']
        del title['BiffCompositeShot']['CompositionAsset']['Layers']['AssetRefLayer']

    title['BiffCompositeShot']['CompositionAsset']['CompositionTemplate']['TemplateProperty'] = []
    title['BiffCompositeShot']['CompositionAsset']['CompositionTemplate']['TreeNode']['BaseNode']['ChildNodes'][
        'ButtonNode'] = []
    title['BiffCompositeShot']['CompositionAsset']['CompositionTemplate']['TreeNode']['BaseNode']['ChildNodes'][
        'TreeNode'] = []
    title['BiffCompositeShot']['CompositionAsset']['Layers']['TextRefLayer'] = []

    text_Count = 0
    for text in key['texts']:
        print("\nTest:", text)
        text_Count += 1
        newTitleObj = create_main(xmlstr)
        text_TemplateProperty = newTitleObj['BiffCompositeShot']['CompositionAsset']['CompositionTemplate'][
            'TemplateProperty']
        text_ButtonNode = \
            newTitleObj['BiffCompositeShot']['CompositionAsset']['CompositionTemplate']['TreeNode']['BaseNode'][
                'ChildNodes']['ButtonNode']
        text_TreeNode = \
            newTitleObj['BiffCompositeShot']['CompositionAsset']['CompositionTemplate']['TreeNode']['BaseNode'][
                'ChildNodes']['TreeNode']
        text_TextRefLayer = newTitleObj['BiffCompositeShot']['CompositionAsset']['Layers']['TextRefLayer']

        text_TextRefLayer_ID = text_TextRefLayer['ID']
        text_Format_ID = text_TextRefLayer['TextBox']['Formats']['Format']['@ID']
        text_TextRefLayer['StartFrame'] = text['FontStartFrame']
        text_TextRefLayer['EndFrame'] = text['FontEndFrame']
        text_TextRefLayer['TextBox']['Tokens']['Tk'] = textcode2token(text['text'], text_Format_ID)
        family, Style, PostscriptName = getFontInfo(text['FontName'])
        text_TextRefLayer['TextBox']['Formats']['Format']['Family'] = family
        text_TextRefLayer['TextBox']['Formats']['Format']['Style'] = Style
        text_TextRefLayer['TextBox']['Formats']['Format']['PostscriptName'] = PostscriptName
        text_TextRefLayer['TextBox']['Formats']['Format']['@Tracking'] = 1.0 + int(text['RowSpace'])/20

        R, G, B = int2RGB(int(text['FontFillColor']))
        text_TextRefLayer['TextBox']['Formats']['Format']['FillColor']['@R'] = R
        text_TextRefLayer['TextBox']['Formats']['Format']['FillColor']['@G'] = G
        text_TextRefLayer['TextBox']['Formats']['Format']['FillColor']['@B'] = B
        text_TextRefLayer['TextBox']['Formats']['Format']['FillColor']['@A'] = '1.0'
        text_TextRefLayer['TextBox']['Formats']['Format']['@Size'] = int(float(text['FontSize']) * 2.276)

        text_TextRefLayer['PropertyManager'] = create_Text_TSF(text)
        text_TextRefLayer['Effects']['Instance']['PropertyManager']['Prop'][1]['Default']['fl'] = 100 * text['FontLeftRange']/(text['FontEndFrame']-text['FontStartFrame'])
        # text_TextRefLayer['Effects']['Instance']['PropertyManager']['Prop'][2]['Default']['fl'] = 100 * text['FontRightRange']/(text['FontEndFrame']-text['FontStartFrame'])
        text_TextRefLayer['Effects']['Instance']['PropertyManager']['Prop'][2]['Default']['fl'] = 10

        text_ButtonNode['BaseNode']['DisplayName'] = 'Edit Text %d'%text_Count
        text_TreeNode[0]['BaseNode']['DisplayName'] = 'Text %d Transform'%text_Count
        text_TreeNode[1]['BaseNode']['DisplayName'] = 'Text %d Animation'%text_Count

        # create_offset(key['name'],text_Count,text_TextRefLayer)  # create the Json file for adjust the text layers.
        text_TextRefLayer = setOffset(key['name'],text_Count,text_TextRefLayer)  # using the Json file for adjusting.


        title['BiffCompositeShot']['CompositionAsset']['CompositionTemplate'][
            'TemplateProperty'] += text_TemplateProperty
        title['BiffCompositeShot']['CompositionAsset']['CompositionTemplate']['TreeNode']['BaseNode']['ChildNodes'][
            'ButtonNode'].append(text_ButtonNode)
        title['BiffCompositeShot']['CompositionAsset']['CompositionTemplate']['TreeNode']['BaseNode']['ChildNodes'][
            'TreeNode'] += text_TreeNode
        title['BiffCompositeShot']['CompositionAsset']['Layers']['TextRefLayer'].append(text_TextRefLayer)

    # move VBG to BG
    print("\nmove VBG to BG")
    if key['WithMedia']:
        AssetRefLayer = title['BiffCompositeShot']['CompositionAsset']['Layers']['AssetRefLayer']
        del title['BiffCompositeShot']['CompositionAsset']['Layers']['AssetRefLayer']
        title['BiffCompositeShot']['CompositionAsset']['Layers']['AssetRefLayer'] = AssetRefLayer

    title_xml = dict2xml(title)
    xml_tga = os.path.join(new, new.split('/')[-1])
    xml = open(xml_tga, 'w')
    xml.write(title_xml)
    xml.close()


def main():
    path = 'Temp'
    # path = 'Temp/LowerThirds 20'
    # path = 'Temp/LowerThirds 15'
    # path = 'Temp/LowerThirds 18'
    # path = 'Temp/LowerThirds 2'
    # path = 'Temp/LowerThirds 7'
    # path = 'Temp/Title 7'
    # path = 'Temp/LowerThirds 1'

    tgaPath = '/Library/Application Support/Wondershare/Wondershare Filmora Pro/Objects/Test'

    files = getAllFiles(path)
    for file in files:
        if "data.xml" in file:
            oldFolder = os.path.dirname(os.path.dirname(file))
            newFolder = os.path.join(tgaPath, oldFolder.split('/')[1] + '.wfptitle')
            setupNewFolder(oldFolder, newFolder)
            create_title(file, newFolder)

            # try:
            #     get_key(file)
            # except:
            #     print('\nerror!!!!\n:',file,'\n')


if __name__ == '__main__':
    main()
    # path = '/Users/ws/Python/ProTitles/Temp/Title 16/Data/data.xml'
    # path = '/Users/ws/Python/ProTitles/Temp/Title 32/Data/data.xml'
    # get_key(path)
