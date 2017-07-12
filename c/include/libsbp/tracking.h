/*
 * Copyright (C) 2015 Swift Navigation Inc.
 * Contact: Fergus Noble <fergus@swift-nav.com>
 *
 * This source is subject to the license found in the file 'LICENSE' which must
 * be be distributed together with this source. All other rights reserved.
 *
 * THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
 * EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.
 */

/*****************************************************************************
 * Automatically generated from yaml/swiftnav/sbp/tracking.yaml
 * with generate.py. Please do not hand edit!
 *****************************************************************************/

/** \defgroup tracking Tracking
 *
 *  * Satellite code and carrier-phase tracking messages from the device.
 * \{ */

#ifndef LIBSBP_TRACKING_MESSAGES_H
#define LIBSBP_TRACKING_MESSAGES_H

#include "common.h"
#include "gnss.h"

#ifdef _MSC_VER
#pragma pack(1)
#endif


/** Detailed signal tracking channel states
 *
 * The tracking message returns a set tracking channel parameters for a
 * single tracking channel useful for debugging issues.
 */
#define SBP_MSG_TRACKING_STATE_DETAILED 0x0011
#ifdef _MSC_VER
typedef struct {
#else
typedef struct __attribute__((packed)) {
#endif
  u64 recv_time;       /**< Receiver clock time. [ns] */
  sbp_gps_time_t tot;             /**< Time of transmission of signal from satellite. TOW only valid when
TOW status is decoded or propagated. WN only valid when week
number valid flag is set.
 */
  u32 P;               /**< Pseudorange observation. Valid only when pseudorange valid flag is
set.
 [2 cm] */
  u16 P_std;           /**< Pseudorange observation standard deviation. Valid only when
pseudorange valid flag is set.
 [2 cm] */
  carrier_phase_t L;               /**< Carrier phase observation with typical sign convention. Valid only
when PLL pessimistic lock is achieved.
 [cycles] */
  u8 cn0;             /**< Carrier-to-Noise density [dB Hz / 4] */
  u16 lock;            /**< Lock time. It is encoded according to DF402 from the RTCM 10403.2
Amendment 2 specification. Valid values range from 0 to 15.
 */
  sbp_gnss_signal_t sid;             /**< GNSS signal identifier. */
  s32 doppler;         /**< Carrier Doppler frequency. [Hz / 16] */
  u16 doppler_std;     /**< Carrier Doppler frequency standard deviation. [Hz / 16] */
  u32 uptime;          /**< Number of seconds of continuous tracking. Specifies how much time
signal is in continuous track.
 [s] */
  s16 clock_offset;    /**< TCXO clock offset. Valid only when valid clock valid flag is set.
 [s / (2 ^ 20)] */
  s16 clock_drift;     /**< TCXO clock drift. Valid only when valid clock valid flag is set.
 [(s / s) / (2 ^ 31)] */
  u16 corr_spacing;    /**< Early-Prompt (EP) and Prompt-Late (PL) correlators spacing. [ns] */
  s8 acceleration;    /**< Acceleration. Valid only when acceleration valid flag is set. [g / 8] */
  u8 sync_flags;      /**< Synchronization status flags. */
  u8 tow_flags;       /**< TOW status flags. */
  u8 track_flags;     /**< Tracking loop status flags. */
  u8 nav_flags;       /**< Navigation data status flags. */
  u8 pset_flags;      /**< Parameters sets flags. */
  u8 misc_flags;      /**< Miscellaneous flags. */
} msg_tracking_state_detailed_t;


/** Signal tracking channel state
 *
 * Tracking channel state for a specific satellite signal and
 * measured signal power.
 */
#ifdef _MSC_VER
typedef struct {
#else
typedef struct __attribute__((packed)) {
#endif
  gnss_signal16_t sid;    /**< GNSS signal being tracked */
  u8 fcn;    /**< Frequency channel number (GLONASS only) */
  u8 cn0;    /**< Carrier-to-Noise density.  Zero implies invalid cn0. [dB Hz / 4] */
} tracking_channel_state_t;


/** Signal tracking channel states
 *
 * The tracking message returns a variable-length array of tracking
 * channel states. It reports status and carrier-to-noise density
 * measurements for all tracked satellites.
 */
#define SBP_MSG_TRACKING_STATE          0x0041
#ifdef _MSC_VER
typedef struct {
#else
typedef struct __attribute__((packed)) {
#endif
  tracking_channel_state_t states[0]; /**< Signal tracking channel state */
} msg_tracking_state_t;


/** Complex correlation structure
 *
 * Structure containing in-phase and quadrature correlation components.
 */
#ifdef _MSC_VER
typedef struct {
#else
typedef struct __attribute__((packed)) {
#endif
  s32 I;    /**< In-phase correlation */
  s32 Q;    /**< Quadrature correlation */
} tracking_channel_correlation_t;


/** Tracking channel correlations
 *
 * When enabled, a tracking channel can output the correlations at each
 * update interval.
 */
#define SBP_MSG_TRACKING_IQ             0x001C
#ifdef _MSC_VER
typedef struct {
#else
typedef struct __attribute__((packed)) {
#endif
  u8 channel;    /**< Tracking channel of origin */
  sbp_gnss_signal_t sid;        /**< GNSS signal identifier */
  tracking_channel_correlation_t corrs[3];   /**< Early, Prompt and Late correlations */
} msg_tracking_iq_t;


/** Deprecated
 *
* Deprecated.
 */
#ifdef _MSC_VER
typedef struct {
#else
typedef struct __attribute__((packed)) {
#endif
  u8 state;    /**< Status of tracking channel */
  u8 prn;      /**< PRN-1 being tracked */
  float cn0;      /**< Carrier-to-noise density [dB Hz] */
} tracking_channel_state_dep_a_t;


/** Deprecated
 *
* Deprecated.
 */
#define SBP_MSG_TRACKING_STATE_DEP_A    0x0016
#ifdef _MSC_VER
typedef struct {
#else
typedef struct __attribute__((packed)) {
#endif
  tracking_channel_state_dep_a_t states[0]; /**< Satellite tracking channel state */
} msg_tracking_state_dep_a_t;


/** Deprecated.
 *
* Deprecated.
 */
#ifdef _MSC_VER
typedef struct {
#else
typedef struct __attribute__((packed)) {
#endif
  u8 state;    /**< Status of tracking channel */
  sbp_gnss_signal_t sid;      /**< GNSS signal being tracked */
  float cn0;      /**< Carrier-to-noise density [dB Hz] */
} tracking_channel_state_dep_b_t;


/** Deprecated.
 *
* Deprecated.
 */
#define SBP_MSG_TRACKING_STATE_DEP_B    0x0013
#ifdef _MSC_VER
typedef struct {
#else
typedef struct __attribute__((packed)) {
#endif
  tracking_channel_state_dep_b_t states[0]; /**< Signal tracking channel state */
} msg_tracking_state_dep_b_t;


/** \} */

#ifdef _MSC_VER
#pragma pack()
#endif

#endif /* LIBSBP_TRACKING_MESSAGES_H */