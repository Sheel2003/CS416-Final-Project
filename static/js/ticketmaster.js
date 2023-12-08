//Adrian: Added js for adding, updating, and deleting an event to the bookmark page
$('.bookmark-button').click(function () {

        const card = $(this).closest('.card')

        const bookmarkData = {
            eventImage: card.find('[id^="event-img"]').attr('src'),
            eventName: card.find('[id^="event-title"]').text(),
            eventLocation: card.find('[id^="address"]').text(),
            eventDate: card.find('[id^="date"]').text(),
            eventTime: card.find('[id^="time"]').text(),
            ticketURL: card.find('[id^="event-url"]').attr('href')
        }

        $.ajax({

            url: "/create/",
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(bookmarkData),
            success: function () {

            },
            error: function () {

            }

        })

    }
);

$('.update-button').click(function () {

        const card = $(this).closest('.card')

        const bookmarkNumber = {
            eventId: card.attr('id'),
        }

        $.ajax({

            url: "/update/",
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(bookmarkNumber),
            success: function () {

            },
            error: function () {

            }

        })
        location.reload()
    }
);
$('.delete-button').click(function () {

        const card = $(this).closest('.card')

        const bookmarkNumber = {
            eventId: card.attr('id'),
        }

        $.ajax({

            url: "/delete/",
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(bookmarkNumber),
            success: function () {

            },
            error: function () {

            }

        })

        location.reload()

    }
);