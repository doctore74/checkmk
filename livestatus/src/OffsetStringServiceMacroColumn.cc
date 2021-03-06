// +------------------------------------------------------------------+
// |             ____ _               _        __  __ _  __           |
// |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
// |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
// |           | |___| | | |  __/ (__|   <    | |  | | . \            |
// |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
// |                                                                  |
// | Copyright Mathias Kettner 2014             mk@mathias-kettner.de |
// +------------------------------------------------------------------+
//
// This file is part of Check_MK.
// The official homepage is at http://mathias-kettner.de/check_mk.
//
// check_mk is free software;  you can redistribute it and/or modify it
// under the  terms of the  GNU General Public License  as published by
// the Free Software Foundation in version 2.  check_mk is  distributed
// in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
// out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
// PARTICULAR PURPOSE. See the  GNU General Public License for more de-
// tails. You should have  received  a copy of the  GNU  General Public
// License along with GNU Make; see the file  COPYING.  If  not,  write
// to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
// Boston, MA 02110-1301 USA.

#include "OffsetStringServiceMacroColumn.h"
#include <optional>
#include "OffsetStringHostMacroColumn.h"
#include "Row.h"
#include "nagios.h"

ServiceMacroExpander::ServiceMacroExpander(const service *svc,
                                           const MonitoringCore *mc)
    : _svc(svc), _cve("_SERVICE", svc->custom_variables, mc) {}

std::optional<std::string> ServiceMacroExpander::expand(
    const std::string &str) {
    if (str == "SERVICEDESC") {
        return from_ptr(_svc->description);
    }
    if (str == "SERVICEDISPLAYNAME") {
        return from_ptr(_svc->display_name);
    }
    if (str == "SERVICEOUTPUT") {
        return from_ptr(_svc->plugin_output);
    }
    if (str == "LONGSERVICEOUTPUT") {
        return from_ptr(_svc->long_plugin_output);
    }
    if (str == "SERVICEPERFDATA") {
        return from_ptr(_svc->perf_data);
    }
    if (str == "SERVICECHECKCOMMAND") {
#ifndef NAGIOS4
        return from_ptr(_svc->service_check_command);
#else
        return from_ptr(_svc->check_command);
#endif  // NAGIOS4
    }
    return _cve.expand(str);
}

std::unique_ptr<MacroExpander> OffsetStringServiceMacroColumn::getMacroExpander(
    Row row) const {
    auto svc = columnData<service>(row);
    return std::make_unique<CompoundMacroExpander>(
        std::make_unique<HostMacroExpander>(svc->host_ptr, _mc),
        std::make_unique<CompoundMacroExpander>(
            std::make_unique<ServiceMacroExpander>(svc, _mc),
            std::make_unique<UserMacroExpander>()));
}
